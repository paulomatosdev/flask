from flask import Blueprint, request, jsonify
from src.app import db
from models.user import User
from models.role import Role
from http import HTTPStatus
from sqlalchemy import inspect
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.utils import requires_roles
from src.app import bcrypt

app = Blueprint("user", __name__, url_prefix="/users")


def _create_user():
    data = request.json
    user = User()
    user.username = data["username"]
    user.email = data["email"]
    user.password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    user.role_id = data["role_id"]
    
    db.session.add(user)
    db.session.commit()
    return user


def _list_users():
    query = db.select(User)
    users = db.session.execute(query).scalars()
    return [
        {
            "id": user.id,
            "username": user.username,
            "role": {
                "id": user.role_id,
                "name": user.role.name,
            },
        }
        for user in users
    ]


@app.route('/<int:user_id>')
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return {
        "id": user.id,
        "username": user.username,
    }


@app.route('/<int:user_id>', methods=["PATCH"])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data = request.json

    mapper = inspect(User)
    assert mapper is not None  

    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])
    db.session.commit()

    return {
        "id": user.id,
        "username": user.username,
    }


@app.route('/<int:user_id>', methods=["DELETE"])
def delete_user(user_id):  
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()

    return "", HTTPStatus.NO_CONTENT


@app.route("", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
@jwt_required()
@requires_roles("admin")
def list_or_create_user():
    user_id = get_jwt_identity()
    user = db.get_or_404(User, user_id)

    if user.role.name != "admin":
        return jsonify({"message": "Usuario não tem acesso"}), HTTPStatus.UNAUTHORIZED
    
    if request.method == "POST":
        _create_user()
        return {"message": "User created!"}, HTTPStatus.CREATED
    else:
        return {"users": _list_users()}