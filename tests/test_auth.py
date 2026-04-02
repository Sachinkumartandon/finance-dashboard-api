def test_register_success(client):
    res = client.post("/auth/register", json={
        "name": "John Doe",
        "email": "john@example.com",
        "password": "secret123",
        "role": "VIEWER"
    })
    assert res.status_code == 201
    data = res.json()
    assert data["email"] == "john@example.com"
    assert data["role"] == "VIEWER"
    assert "password" not in data
    assert "password_hash" not in data


def test_register_duplicate_email(client):
    payload = {"name": "User", "email": "dup@example.com", "password": "pass123"}
    client.post("/auth/register", json=payload)
    res = client.post("/auth/register", json=payload)
    assert res.status_code == 409


def test_register_short_password(client):
    res = client.post("/auth/register", json={
        "name": "User", "email": "x@example.com", "password": "abc"
    })
    assert res.status_code == 422


def test_login_success(client):
    client.post("/auth/register", json={
        "name": "User", "email": "user@example.com", "password": "pass123"
    })
    res = client.post("/auth/login", json={"email": "user@example.com", "password": "pass123"})
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post("/auth/register", json={
        "name": "User", "email": "user2@example.com", "password": "correct"
    })
    res = client.post("/auth/login", json={"email": "user2@example.com", "password": "wrong"})
    assert res.status_code == 401


def test_login_unknown_email(client):
    res = client.post("/auth/login", json={"email": "ghost@example.com", "password": "any"})
    assert res.status_code == 401
