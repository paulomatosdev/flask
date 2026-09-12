import pytest
from src.app import create_app, db, User, Role, bcrypt

@pytest.fixture
def app():
    app = create_app(enviroment="testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.rollback()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def role(client):
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()
    return role


@pytest.fixture
def user(client, role):
    user = User(
        username="test_user",
        email="test_user@example.com",
        password=bcrypt.generate_password_hash("test_password").decode("utf-8"),
        role_id=role.id,
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def access_token(client, user):
    response = client.post(
        "/auth/login",
        json={"username": user.username, "password": "test_password"},
    )
    return response.json["access_token"]


