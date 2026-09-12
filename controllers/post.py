from flask import Blueprint, request, jsonify
from src.app import db
from models.post import Post
from http import HTTPStatus
from sqlalchemy import inspect
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.utils import requires_roles

app = Blueprint("post", __name__, url_prefix="/posts")


def _create_post():
    data = request.json
    post = Post()
    post.title = data["title"]
    post.content = data["content"]
    post.author_id = data["author_id"]
    
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
            "content": post.content,
            "author": {
                "id": post.author.id,
                "username": post.author.username,
            },
        }
        for post in posts
    ]


@app.route('/<int:post_id>')
def get_post(post_id):
    post = db.get_or_404(Post, post_id)
    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author_id": post.author_id,
    }


@app.route('/<int:post_id>', methods=["PATCH"])
def update_post(post_id):
    post = db.get_or_404(Post, post_id)
    data = request.json

    mapper = inspect(Post)
    assert mapper is not None

    for column in mapper.attrs:
        if column.key in data:
            setattr(post, column.key, data[column.key])
    db.session.commit()

    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
    }


@app.route('/<int:post_id>', methods=["DELETE"])
def delete_post(post_id):
    post = db.get_or_404(Post, post_id)
    db.session.delete(post)
    db.session.commit()

    return "", HTTPStatus.NO_CONTENT


@app.route("/", methods=["GET", "POST"])
@jwt_required()
@requires_roles("admin")
def list_or_create_post():
    if request.method == "POST":
        _create_post()
        return {"message": "post created"}, HTTPStatus.CREATED
    else:
        return {"identity": get_jwt_identity(), "Posts": _list_post()}