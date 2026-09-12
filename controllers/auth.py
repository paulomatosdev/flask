from flask import Blueprint, request

from sqlalchemy import inspect
from http import HTTPStatus
from src.app import bcrypt, db, User

from flask import jsonify
from flask import request

from flask_jwt_extended import create_access_token

def _valid_password(password, pw_hash):
    return bcrypt.check_password_hash(pw_hash, password)

app = Blueprint("auth", __name__, url_prefix="/auth")

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = db.session.execute(db.select(User).where(User.username==username)).scalar()
    if not user or not _valid_password(password, user.password):
        return jsonify({"message": "erro no usuario ou senha"}), HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(identity=str(user.id))
    return jsonify(access_token=access_token)