from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from models.base import db
from models.user import User
from models.role import Role
from models.post import Post
from flask_bcrypt import Bcrypt
import os

migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app(enviroment=os.environ.get('ENVIROMENT', 'development')):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(f"src.config.{enviroment.title()}Config")

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass    


    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # registro de blueprints
    from controllers import user, auth, role, post
    
    
    app.register_blueprint(user.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(role.app)
    app.register_blueprint(post.app)

    return app


app = create_app()