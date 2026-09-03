

from flask_jwt_extended import get_jwt_identity
from src.app import User,db
from http import HTTPStatus
from functools import wraps

def requires_roles(role_name):
    def decorador(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user_id = get_jwt_identity()
            user = db.get_or_404(User, user_id)

            if user.role.name != role_name:
                return {"message": "Usuário não tem acesso."}, HTTPStatus.FORBIDDEN
            return f(*args, **kwargs)
        
        return wrapped
    return decorador

def eleva_quadrado(x):
    return x ** 2