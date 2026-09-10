"""Flask configuration"""
import os
from datetime import timedelta

# Get config from environment variables
DEBUG = os.getenv("FLASK_DEBUG", False)
TESTING = os.getenv("FLASK_TESTING", False)
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-super-secret-key")
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///db.sqlite")
SQLALCHEMY_TRACK_MODIFICATIONS = False

# JWT Configuration
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
