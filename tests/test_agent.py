import os
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from backend.app.main import app
from backend.app.models.db import SQLModel, engine

@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Create a test user and login to get token
        await ac.post("/api/auth/signup", json={"email": "agent@test.com", "password": "Password123"})
        res = await ac.post("/api/auth/login", json={"email": "agent@test.com", "password": "Password123"})
        token = res.json()["access_token"]
        ac.headers = {"Authorization": f"Bearer {token}"}
        yield ac

@pytest.mark.asyncio
async def test_feasibility_rejection(client):
    # Testing the Analyzer node with an unreasonable request
    response = await client.post(
        "/api/chat",
        json={
            "query": "Build a complex 3D MMORPG with a custom physics engine in C++",
            "mode": "project"
        }
    )
    assert response.status_code == 200
    # The output should contain the "Project Not Feasible" message from the chat node
    assert "Project Not Feasible" in response.json()["response"]

@pytest.mark.asyncio
async def test_chat_mode_no_project(client):
    # Testing that 'chat' mode doesn't trigger project creation
    response = await client.post(
        "/api/chat",
        json={
            "query": "Hello, how are you?",
            "mode": "chat"
        }
    )
    assert response.status_code == 200
    assert response.json()["project_name"] is None
    assert response.json()["files"] == []

@pytest.mark.asyncio
async def test_project_mode_success(client):
    # Testing a simple feasible project
    response = await client.post(
        "/api/chat",
        json={
            "query": "Build a simple greeting website with a blue background",
            "mode": "project"
        }
    )
    assert response.status_code == 200
    # Should have a project name and index.html
    assert response.json()["project_name"] is not None
    assert "index.html" in response.json()["files"]
    assert "response" in response.json()
    assert "Successfully wrote" in response.json()["response"]
