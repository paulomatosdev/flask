from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from models.models import db

migrate = Migrate()
jwt = JWTManager()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URL='sqlite:///db.sqlite',
        JWT_SECRET_KEY = "super-secret",
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        
        app.config.from_mapping(test_config)


    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # registro de blueprints
    from controllers import user, auth, role, post
    
    
    app.register_blueprint(user.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(role.app)
    app.register_blueprint(post.app)

    return app


app = create_app()