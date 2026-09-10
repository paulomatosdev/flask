import pytest
from src.app import create_app, db, User, Role

@pytest.fixture
def app():
    app = create_app(
        {
            "SECRET_KEY": "test",
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "WT_SECRET_KEY": "test",
        }
    )
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
        password="test_password",
        role_id=role.id,
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def access_token(client, user):
    response = client.post(
        "/auth/login",
        json={"username": user.username, "password": user.password},
    )
    return response.json["access_token"]


