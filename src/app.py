from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

from models.base import db
from HttpException import HTTPException

import json
import os


migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()


def create_app(environment=os.environ.get("ENVIRONMENT", "development")):

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(
        f"src.config.{environment.title()}Config"
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Registro dos blueprints
    from controllers import user, auth, role, post

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        response = e.get_response()

        response.data = json.dumps({
            "code": e.code,
            "name": e.name,
            "description": e.description,
        })

        response.content_type = "application/json"

        return response

    app.register_blueprint(user.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(role.app)
    app.register_blueprint(post.app)

    return app


app = create_app()