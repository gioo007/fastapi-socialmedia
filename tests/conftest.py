'''
Conftest contains all the fixtures that are used across the tests. 
It is a good place to put common setup code for your tests, 
such as creating a test database, setting up a test client, and creating test data.
'''

from fastapi.testclient import TestClient
import pytest
from apps.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from apps.config import settings
from apps.db import get_db, Base
from apps.oauth2 import create_access_token
from apps import models

sqlalchemy_database_url = f"postgresql://{settings.postgres_user}:{settings.postgres_password}@localhost/{settings.postgres_db}_test"
engine = create_engine(sqlalchemy_database_url)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def session():
    print("my session fixture ran")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    

@pytest.fixture()
def test_user(client):
    user_data = {"first_name": "Test", "last_name": "User", "email": "test@example.com", "password": "password123"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]  # attach plain password for login tests
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"first_name": "Gio", "last_name": "User", "email": "gio@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user2['id']
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts