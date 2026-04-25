import os
import shutil
import zipfile
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import FileResponse
from sqlmodel import Session, select, desc
from ..models.db import User, Project, ChatSession, ChatMessage, get_session
from ..models.schemas import ChatRequest, ChatResponse, SessionRead, MessageRead
from ..services.agent import agent_app
from ..core.auth_utils import get_current_user
from langchain_core.messages import HumanMessage, AIMessage

from ..core.config import settings

router = APIRouter()

# Projects folder is at the project root
PROJECTS_DIR = "projects"

@router.get("/config")
async def get_config():
    """Returns the current system default model and provider."""
    return {
        "llm_provider": settings.LLM_PROVIDER,
        "default_model": settings.GROQ_MODEL_NAME if settings.LLM_PROVIDER == "groq" else settings.OPENAI_MODEL_NAME
    }

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    try:
        # 1. Handle Session
        chat_sess = None
        if request.session_id:
            chat_sess = db.get(ChatSession, request.session_id)
            if not chat_sess or chat_sess.user_id != current_user.id:
                raise HTTPException(status_code=404, detail="Session not found")
        
        # 2. Fetch existing context
        existing_files = {}
        history = []
        project_id = chat_sess.project_id if chat_sess else None
        project_name = request.project_name
        
        if chat_sess:
            if chat_sess.project:
                project_name = chat_sess.project.name
            
            # Fetch message history (Limit to last 10 messages for context efficiency)
            msg_statement = select(ChatMessage).where(ChatMessage.session_id == chat_sess.id).order_by(desc(ChatMessage.created_at)).limit(10)
            prev_msgs = db.exec(msg_statement).all()
            # Reverse because we fetched them in desc order
            for m in reversed(prev_msgs):
                if m.role == "user":
                    history.append(HumanMessage(content=m.content))
                else:
                    history.append(AIMessage(content=m.content))

        if project_name:
            statement = select(Project).where(Project.name == project_name, Project.user_id == current_user.id)
            project = db.exec(statement).first()
            
            if project:
                project_id = project.id
                proj_path = os.path.join(PROJECTS_DIR, project_name)
                if os.path.exists(proj_path):
                    total_chars = 0
                    MAX_CHARS = 30000  # Safeguard total context size
                    for root, _, files in os.walk(proj_path):
                        for file in files:
                            if total_chars > MAX_CHARS: break
                            
                            # Only read text-based source files
                            if not file.endswith(('.html', '.js', '.css', '.py', '.txt', '.md')):
                                continue
                                
                            rel_path = os.path.relpath(os.path.join(root, file), proj_path)
                            with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                                content = f.read()
                                # Truncate individual files if they are massive
                                if len(content) > 10000:
                                    content = content[:10000] + "... [TRUNCATED]"
                                existing_files[rel_path] = content
                                total_chars += len(content)

        # 3. Invoke Agent
        inputs = {
            "messages": history + [HumanMessage(content=request.query)],
            "mode": request.mode,
            "project_name": project_name or "",
            "files": {},
            "existing_files": existing_files,
            "project_type": "",
            "status": "initializing",
            "summary": "",
            "is_feasible": True,
            "feasibility_reason": "",
            "retry_count": 0,
            "validation_error": "",
            "model_name": request.model_name
        }
        
        result = await agent_app.ainvoke(inputs)
        last_message = result["messages"][-1]
        res_project_name = result.get("project_name")
        res_summary = result.get("summary", "")
        generated_files = result.get("files", {})
        
        # 4. Save/Update Project
        if request.mode == "project" and res_project_name and generated_files:
            statement = select(Project).where(Project.name == res_project_name, Project.user_id == current_user.id)
            db_project = db.exec(statement).first()
            if not db_project:
                db_project = Project(
                    name=res_project_name,
                    project_type=result.get("project_type", "web"),
                    path=os.path.join(PROJECTS_DIR, res_project_name),
                    user_id=current_user.id
                )
                db.add(db_project)
                db.commit()
                db.refresh(db_project)
            project_id = db_project.id

        # 5. Save Session and Messages
        if not chat_sess:
            session_name = res_project_name or (request.query[:30] + "...")
            chat_sess = ChatSession(name=session_name, user_id=current_user.id, project_id=project_id)
            db.add(chat_sess)
            db.commit()
            db.refresh(chat_sess)
            
        final_response = res_summary if res_summary else last_message.content
        user_msg = ChatMessage(session_id=chat_sess.id, role="user", content=request.query)
        ai_msg = ChatMessage(session_id=chat_sess.id, role="assistant", content=final_response)
        db.add(user_msg)
        db.add(ai_msg)
        db.commit()

        preview_url = None
        final_project_name = res_project_name or project_name
        # Only show preview if an index.html was actually written in this turn
        if final_project_name and "index.html" in generated_files:
            preview_url = f"http://localhost:8000/view-projects/{final_project_name}/index.html"
            
        return ChatResponse(
            response=final_response,
            session_id=chat_sess.id,
            project_name=final_project_name,
            files=list(generated_files.keys()),
            preview_url=preview_url
        )
    except Exception as e:
        if isinstance(e, HTTPException): raise e
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions", response_model=List[SessionRead])
async def get_sessions(current_user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    """Returns all chat sessions for the current user."""
    statement = select(ChatSession).where(ChatSession.user_id == current_user.id).order_by(desc(ChatSession.created_at))
    return db.exec(statement).all()

@router.get("/sessions/{session_id}/messages", response_model=List[MessageRead])
async def get_session_messages(
    session_id: int, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_session)
):
    """Returns all messages for a specific session."""
    session = db.get(ChatSession, session_id)
    if not session or session.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Session not found")
    
    statement = select(ChatMessage).where(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at)
    return db.exec(statement).all()

@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Deletes a specific chat session and its messages."""
    session = db.get(ChatSession, session_id)
    if not session or session.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Session not found")
    
    try:
        db.delete(session)
        db.commit()
        return {"detail": "Session deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete session: {str(e)}")

@router.get("/projects")
async def get_projects(current_user: User = Depends(get_current_user), db: Session = Depends(get_session)):
    """Returns a list of project names for the current user."""
    statement = select(Project).where(Project.user_id == current_user.id)
    projects = db.exec(statement).all()
    return [p.name for p in projects]

@router.get("/projects/{project_name}")
async def get_project_details(
    project_name: str, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Returns details about a specific project."""
    statement = select(Project).where(Project.name == project_name, Project.user_id == current_user.id)
    project = db.exec(statement).first()
    
    if not project:
        raise HTTPException(status_code=404, detail=f"Project '{project_name}' not found")
    
    file_list = []
    if os.path.exists(project.path):
        for root, _, files in os.walk(project.path):
            for file in files:
                rel_path = os.path.relpath(os.path.join(root, file), project.path)
                file_list.append(rel_path)
    
    return {
        "project_name": project.name,
        "files": sorted(file_list)
    }

@router.get("/projects/{project_name}/download")
async def download_project(
    project_name: str, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Compresses the contents of projects/{project_name}/ into a ZIP file."""
    statement = select(Project).where(Project.name == project_name, Project.user_id == current_user.id)
    project = db.exec(statement).first()
    
    if not project or not os.path.exists(project.path):
        raise HTTPException(status_code=404, detail=f"Project '{project_name}' not found")
    
    zip_path = os.path.join(PROJECTS_DIR, f"{project_name}.zip")
    
    try:
        if os.path.exists(zip_path):
            os.remove(zip_path)
            
        archive_path = shutil.make_archive(
            base_name=os.path.join(PROJECTS_DIR, project_name), 
            format='zip', 
            root_dir=project.path
        )
        
        return FileResponse(
            path=archive_path,
            media_type='application/zip',
            filename=f"{project_name}.zip"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create download: {str(e)}")

@router.delete("/projects/{project_name}")
async def delete_project(
    project_name: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Deletes a project, its files, and its associated chat sessions."""
    statement = select(Project).where(Project.name == project_name, Project.user_id == current_user.id)
    project = db.exec(statement).first()
    
    if not project:
        raise HTTPException(status_code=404, detail=f"Project '{project_name}' not found")
    
    try:
        if os.path.exists(project.path):
            shutil.rmtree(project.path)
            
        zip_path = os.path.join(PROJECTS_DIR, f"{project_name}.zip")
        if os.path.exists(zip_path):
            os.remove(zip_path)
            
        db.delete(project)
        db.commit()
        
        return {"detail": f"Project '{project_name}' deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to delete project: {str(e)}")
