from http import HTTPStatus
from sqlalchemy import func
from src.app import User, Role, db




def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def test_get_user_success(client, user):
    response = client.get(f"/users/{user.id}")

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "id": user.id,
        "username": user.username,
    }


def test_get_user_not_found(client, role):
    non_existent_id = 1
    response = client.get(f"/users/{non_existent_id}")

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_create_user(client, user, role, access_token):
    payload = {
        "username": "user2",
        "email": "user2@example.com",
        "password": "user2",
        "role_id": role.id,
    }

    response = client.post("/users/", json=payload, headers=auth_header(access_token))

    assert response.status_code == HTTPStatus.CREATED
    assert response.json == {"message": "User created!"}
    assert db.session.execute(func.count(User.id)).scalar() == 2


def test_list_users(client, user, role, access_token):
    response = client.get("/users", headers=auth_header(access_token))

    assert response.status_code == HTTPStatus.OK
    assert response.json == {
        "users": [
            {
                "id": user.id,
                "username": user.username,
                "role": {"id": role.id, "name": role.name},
            }
        ]
    }