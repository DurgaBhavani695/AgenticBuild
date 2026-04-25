import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .api.routes import router as api_router
from .api.auth import router as auth_router
from .models.db import create_db_and_tables

app = FastAPI(title="AgenticBuild API")

# Create DB tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create projects directory if it doesn't exist
os.makedirs("projects", exist_ok=True)

# Mount the projects folder to serve index.html files
app.mount("/view-projects", StaticFiles(directory="projects"), name="projects")

app.include_router(api_router, prefix="/api")
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
