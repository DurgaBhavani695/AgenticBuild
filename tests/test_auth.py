import os
# Set DATABASE_URL before any other imports that might load the engine
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from backend.app.main import app
from backend.app.models.db import SQLModel, engine

@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    # Set up the database
    SQLModel.metadata.create_all(engine)
    yield
    # No need to delete file for in-memory DB
    SQLModel.metadata.drop_all(engine)

@pytest_asyncio.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_signup_valid(client):
    response = await client.post(
        "/api/auth/signup",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

@pytest.mark.asyncio
async def test_signup_duplicate_email(client):
    # First signup
    await client.post(
        "/api/auth/signup",
        json={"email": "duplicate@example.com", "password": "password123"}
    )
    # Duplicate signup
    response = await client.post(
        "/api/auth/signup",
        json={"email": "duplicate@example.com", "password": "password123"}
    )
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_signup_invalid_email(client):
    response = await client.post(
        "/api/auth/signup",
        json={"email": "invalid-email", "password": "password123"}
    )
    assert response.status_code == 422 # Pydantic validation failure

@pytest.mark.asyncio
async def test_login_valid(client):
    # Signup first
    await client.post(
        "/api/auth/signup",
        json={"email": "login@example.com", "password": "password123"}
    )
    # Login
    response = await client.post(
        "/api/auth/login",
        json={"email": "login@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_login_wrong_password(client):
    # Signup first
    await client.post(
        "/api/auth/signup",
        json={"email": "wrongpass@example.com", "password": "password123"}
    )
    # Login with wrong password
    response = await client.post(
        "/api/auth/login",
        json={"email": "wrongpass@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
