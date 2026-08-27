from flask import Blueprint, request
from src.app import User, db
from sqlalchemy import inspect
from http import HTTPStatus

from flask import jsonify
from flask import request

from flask_jwt_extended import create_access_token


app = Blueprint("auth", __name__, url_prefix="/auth")

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "erro no usuario ou senha"}), HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)