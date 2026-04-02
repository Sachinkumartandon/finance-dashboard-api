"""
Shared test fixtures.
Uses an in-memory SQLite database — no PostgreSQL needed to run tests.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

SQLITE_URL = "sqlite:///./test.db"

engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client():
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


@pytest.fixture
def admin_token(client):
    client.post("/auth/register", json={
        "name": "Admin", "email": "admin@test.com",
        "password": "admin123", "role": "ADMIN"
    })
    res = client.post("/auth/login", json={"email": "admin@test.com", "password": "admin123"})
    return res.json()["access_token"]


@pytest.fixture
def analyst_token(client):
    client.post("/auth/register", json={
        "name": "Analyst", "email": "analyst@test.com",
        "password": "analyst123", "role": "ANALYST"
    })
    res = client.post("/auth/login", json={"email": "analyst@test.com", "password": "analyst123"})
    return res.json()["access_token"]


@pytest.fixture
def viewer_token(client):
    client.post("/auth/register", json={
        "name": "Viewer", "email": "viewer@test.com",
        "password": "viewer123", "role": "VIEWER"
    })
    res = client.post("/auth/login", json={"email": "viewer@test.com", "password": "viewer123"})
    return res.json()["access_token"]
