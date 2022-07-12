import pytest
from app import models


@pytest.mark.parametrize("email, status_code", [
    ("test@gmail.com", 201),
    ("testgmail.com", 422),
])
def test_create_user(client, email, status_code):
    res = client.post(
        "/api/v1/user/create/", 
        json={"name": "test", "email": email, "password": "123"}
    )
    assert res.status_code == status_code
    assert res.status_code == status_code


def test_login(mock_user, client):
    res = client.post(
        "/api/v1/auth/login/", 
        data={"username": "test@gmail.com", "password": "123"}
    )
    data = res.json()
    assert data['token_type'] == 'Bearer'
    assert res.status_code == 200


def test_get_user(mock_login_user, client):
    res = client.get(
        "/api/v1/user/1/",
        headers={"Authorization": f"Bearer {mock_login_user['access_token']}"}
    )
    data = res.json()
    assert data['user_id'] == 1
    assert res.status_code == 200


def test_delete_user(mock_login_user, client, session):
    res = client.delete(
        "/api/v1/user/delete/1/",
        headers={"Authorization": f"Bearer {mock_login_user['access_token']}"}
    )
    assert session.query(models.UserModel).get(1) == None
    assert res.status_code == 204


def test_change_password(mock_login_user, client):
    data = {"old_password": "123", "new_password": "new"}
    res = client.put(
        "/api/v1/user/change_password/",
        json=data,
        headers={"Authorization": f"Bearer {mock_login_user['access_token']}"}
    )
    assert res.status_code == 204


def test_wrong_change_password(mock_login_user, client):
    data = {"old_password": "wrong", "new_password": "new"}
    res = client.put(
        "/api/v1/user/change_password/",
        json=data,
        headers={"Authorization": f"Bearer {mock_login_user['access_token']}"}
    )
    assert res.status_code == 400


def test_create_admin(mock_login_admin, client):
    res = client.post(
        "/api/v1/user/create/admin/", 
        json={"name": "admin", "email": "admin@gmail.com", "password": "123"},
        headers={"Authorization": f"Bearer {mock_login_admin['access_token']}"}
    )
    assert res.status_code == 201


def test_create_admin_no_auth(client):
    res = client.post(
        "/api/v1/user/create/admin/", 
        json={"name": "admin", "email": "admin@gmail.com", "password": "123"},
    )
    assert res.status_code == 401

