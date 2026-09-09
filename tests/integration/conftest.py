import pytest
from src.app import create_app

@pytest.fixture()
def app():
    app = create_app(
        {
            "SECRET_KEY": "dev",
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "WT_SECRET_KEY": "super-secret"
        }
    )
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()

