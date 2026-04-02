def auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_get_my_profile(client, viewer_token):
    res = client.get("/users/me", headers=auth(viewer_token))
    assert res.status_code == 200
    assert res.json()["email"] == "viewer@test.com"


def test_admin_can_list_users(client, admin_token):
    res = client.get("/users/", headers=auth(admin_token))
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_viewer_cannot_list_users(client, viewer_token):
    res = client.get("/users/", headers=auth(viewer_token))
    assert res.status_code == 403


def test_analyst_cannot_list_users(client, analyst_token):
    res = client.get("/users/", headers=auth(analyst_token))
    assert res.status_code == 403


def test_admin_can_update_user_role(client, admin_token, viewer_token):
    # Get viewer's id
    me_res = client.get("/users/me", headers=auth(viewer_token))
    viewer_id = me_res.json()["id"]

    res = client.patch(f"/users/{viewer_id}", json={"role": "ANALYST"}, headers=auth(admin_token))
    assert res.status_code == 200
    assert res.json()["role"] == "ANALYST"


def test_admin_can_deactivate_user(client, admin_token, viewer_token):
    me_res = client.get("/users/me", headers=auth(viewer_token))
    viewer_id = me_res.json()["id"]

    res = client.patch(f"/users/{viewer_id}", json={"is_active": False}, headers=auth(admin_token))
    assert res.status_code == 200
    assert res.json()["is_active"] is False


def test_admin_cannot_delete_self(client, admin_token):
    me_res = client.get("/users/me", headers=auth(admin_token))
    admin_id = me_res.json()["id"]
    res = client.delete(f"/users/{admin_id}", headers=auth(admin_token))
    assert res.status_code == 400


def test_get_nonexistent_user(client, admin_token):
    res = client.get("/users/99999", headers=auth(admin_token))
    assert res.status_code == 404
