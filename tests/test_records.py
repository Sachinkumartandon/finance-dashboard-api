RECORD_PAYLOAD = {
    "amount": 1500.00,
    "type": "income",
    "category": "Salary",
    "date": "2024-06-01",
    "notes": "June salary"
}


def auth(token):
    return {"Authorization": f"Bearer {token}"}


# ── Create ────────────────────────────────────────────────────────────────────

def test_admin_can_create_record(client, admin_token):
    res = client.post("/records/", json=RECORD_PAYLOAD, headers=auth(admin_token))
    assert res.status_code == 201
    data = res.json()
    assert data["amount"] == 1500.00
    assert data["category"] == "Salary"


def test_analyst_can_create_record(client, analyst_token):
    res = client.post("/records/", json=RECORD_PAYLOAD, headers=auth(analyst_token))
    assert res.status_code == 201


def test_viewer_cannot_create_record(client, viewer_token):
    res = client.post("/records/", json=RECORD_PAYLOAD, headers=auth(viewer_token))
    assert res.status_code == 403


def test_create_record_negative_amount(client, admin_token):
    payload = {**RECORD_PAYLOAD, "amount": -100}
    res = client.post("/records/", json=payload, headers=auth(admin_token))
    assert res.status_code == 422


def test_unauthenticated_cannot_create(client):
    res = client.post("/records/", json=RECORD_PAYLOAD)
    assert res.status_code in [401, 403]


# ── Read ──────────────────────────────────────────────────────────────────────

def test_viewer_can_list_records(client, viewer_token, admin_token):
    client.post("/records/", json=RECORD_PAYLOAD, headers=auth(admin_token))
    res = client.get("/records/", headers=auth(viewer_token))
    assert res.status_code == 200
    data = res.json()
    assert "results" in data
    assert data["total"] >= 1


def test_filter_by_type(client, admin_token):
    client.post("/records/", json=RECORD_PAYLOAD, headers=auth(admin_token))
    client.post("/records/", json={**RECORD_PAYLOAD, "type": "expense", "category": "Rent"}, headers=auth(admin_token))
    res = client.get("/records/?type=income", headers=auth(admin_token))
    assert res.status_code == 200
    for record in res.json()["results"]:
        assert record["type"] == "income"


def test_pagination(client, admin_token):
    for _ in range(5):
        client.post("/records/", json=RECORD_PAYLOAD, headers=auth(admin_token))
    res = client.get("/records/?page=1&limit=2", headers=auth(admin_token))
    assert res.status_code == 200
    data = res.json()
    assert len(data["results"]) <= 2
    assert data["page"] == 1


# ── Update ────────────────────────────────────────────────────────────────────

def test_admin_can_update_record(client, admin_token):
    create_res = client.post("/records/", json=RECORD_PAYLOAD, headers=auth(admin_token))
    record_id = create_res.json()["id"]
    res = client.put(f"/records/{record_id}", json={"amount": 2000.00}, headers=auth(admin_token))
    assert res.status_code == 200
    assert res.json()["amount"] == 2000.00


def test_analyst_cannot_update_record(client, admin_token, analyst_token):
    create_res = client.post("/records/", json=RECORD_PAYLOAD, headers=auth(admin_token))
    record_id = create_res.json()["id"]
    res = client.put(f"/records/{record_id}", json={"amount": 999}, headers=auth(analyst_token))
    assert res.status_code == 403


# ── Delete ────────────────────────────────────────────────────────────────────

def test_admin_can_soft_delete(client, admin_token):
    create_res = client.post("/records/", json=RECORD_PAYLOAD, headers=auth(admin_token))
    record_id = create_res.json()["id"]

    del_res = client.delete(f"/records/{record_id}", headers=auth(admin_token))
    assert del_res.status_code == 200

    # Deleted record should not appear in list
    list_res = client.get("/records/", headers=auth(admin_token))
    ids = [r["id"] for r in list_res.json()["results"]]
    assert record_id not in ids


def test_analyst_cannot_delete(client, admin_token, analyst_token):
    create_res = client.post("/records/", json=RECORD_PAYLOAD, headers=auth(admin_token))
    record_id = create_res.json()["id"]
    res = client.delete(f"/records/{record_id}", headers=auth(analyst_token))
    assert res.status_code == 403
