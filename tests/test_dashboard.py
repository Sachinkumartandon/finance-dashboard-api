INCOME = {"amount": 3000, "type": "income", "category": "Salary", "date": "2024-06-01"}
EXPENSE = {"amount": 800, "type": "expense", "category": "Rent", "date": "2024-06-05"}


def auth(token):
    return {"Authorization": f"Bearer {token}"}


def seed_records(client, token):
    client.post("/records/", json=INCOME, headers=auth(token))
    client.post("/records/", json=EXPENSE, headers=auth(token))


# ── Summary ───────────────────────────────────────────────────────────────────

def test_summary_returns_correct_values(client, admin_token):
    seed_records(client, admin_token)
    res = client.get("/dashboard/summary", headers=auth(admin_token))
    assert res.status_code == 200
    data = res.json()
    assert data["total_income"] == 3000.0
    assert data["total_expenses"] == 800.0
    assert data["net_balance"] == 2200.0
    assert data["total_records"] == 2


def test_viewer_can_see_summary(client, viewer_token):
    res = client.get("/dashboard/summary", headers=auth(viewer_token))
    assert res.status_code == 200


def test_summary_empty_db(client, admin_token):
    res = client.get("/dashboard/summary", headers=auth(admin_token))
    assert res.status_code == 200
    data = res.json()
    assert data["total_income"] == 0.0
    assert data["net_balance"] == 0.0


# ── By Category ───────────────────────────────────────────────────────────────

def test_by_category(client, admin_token):
    seed_records(client, admin_token)
    res = client.get("/dashboard/by-category", headers=auth(admin_token))
    assert res.status_code == 200
    data = res.json()
    assert "income" in data
    assert "expenses" in data
    assert any(item["category"] == "Salary" for item in data["income"])
    assert any(item["category"] == "Rent" for item in data["expenses"])


# ── Trends ────────────────────────────────────────────────────────────────────

def test_trends_analyst_access(client, analyst_token):
    res = client.get("/dashboard/trends", headers=auth(analyst_token))
    assert res.status_code == 200


def test_trends_viewer_forbidden(client, viewer_token):
    res = client.get("/dashboard/trends", headers=auth(viewer_token))
    assert res.status_code == 403


def test_trends_admin_access(client, admin_token):
    seed_records(client, admin_token)
    res = client.get("/dashboard/trends?months=12", headers=auth(admin_token))
    assert res.status_code == 200
    assert isinstance(res.json(), list)


# ── Recent Activity ───────────────────────────────────────────────────────────

def test_recent_activity(client, admin_token):
    seed_records(client, admin_token)
    res = client.get("/dashboard/recent?limit=5", headers=auth(admin_token))
    assert res.status_code == 200
    data = res.json()
    assert "records" in data
    assert len(data["records"]) <= 5


def test_unauthenticated_cannot_see_dashboard(client):
    res = client.get("/dashboard/summary")
    assert res.status_code in [401, 403]
