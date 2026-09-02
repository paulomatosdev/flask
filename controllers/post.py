from flask import Blueprint, request, jsonify
from src.app import Post, db, User
from http import HTTPStatus
from sqlalchemy import inspect
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.utils import requires_roles

app = Blueprint("post", __name__, url_prefix="/posts")


def _create_post():
    data = request.json
    post = Post(title = data["title"],
                content = data["content"],
                author_id = data["author_id"])
    db.session.add(post)
    db.session.commit()
    return post


def _list_post():
    query = db.select(Post)
    posts = db.session.execute(query).scalars()
    return [
        {
            "id": post.id,
            "title": post.title,
            "body": post.body,
            "author": {
                "id": post.author.id,
                "username": post.author.username,
            },
        }
        for post in posts
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


@app.route("/", methods=["GET", "POST"])
@jwt_required()
@requires_roles("admin")
def list_or_create_user():
    user_id = get_jwt_identity()
    user = db.get_or_404(User, user_id)

    if user.role.name != "admin":
        return jsonify({"message": "Usuario não tem acesso"}), HTTPStatus.UNAUTHORIZED
    
    if request.method == "POST":
        _create_post()
        return {"message": "post created"}, HTTPStatus.CREATED
    else:
        return {"identity": get_jwt_identity(), "Users": _list_post()}