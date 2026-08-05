from jose import jwt
import pytest
from .conftest import client
from apps.config import settings
from apps import schemas

def test_root(client):
    response = client.get("/")
    assert response.json().get("message") == "I love you holly❤️"
    assert response.status_code == 200

def test_create_user(client):
    response = client.post("/users/", json={"first_name": "Test", "last_name": "User", "email": "test@example.com", "password": "password123"})
    new_user = schemas.UserResponse(**response.json())
    assert new_user.email == "test@example.com"
    assert response.status_code == 201

def test_login(client, test_user): #note that test_user already depends on client, but its there for clarity
    response = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_response.token_type == "bearer"
    assert response.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrong@example.com', 'password123', 403),
    ('test@example.com', 'wrongpassword', 403),
    ('wrong@example.com', 'wrongpassword', 403)
])
def test_incorrect_login(client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    assert res.json().get('detail') == 'Invalid Credentials'