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
