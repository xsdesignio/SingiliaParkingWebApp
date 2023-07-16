from flask import redirect, request, session, url_for, jsonify
from functools import wraps
from users.models.user_model import UserModel

from users.entities.user import User


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if 'name' not in session:
            redirect_url = url_for('auth.login_page')
            return redirect(redirect_url)
        return function(*args, **kwargs)
    return wrapper



def role_required(role:str):
    def decorator(function):
        def wrapper(*args, **kwargs):
            if 'name' not in session or session['role'] != role.upper():
                return {}, 500 # Redirige a la página de inicio de sesión
            return function(*args, **kwargs)
        return wrapper
    return decorator




def login_user(email, password) -> bool:
    '''
        Return an User object if email and password are corrects
    '''
    # Obtaining user
    user: User = UserModel.get_validated_user(email, password)

    if user != None:
        session['id'] = user.id
        session['role'] = user.role.name
        session['email'] = user.email
        session['name'] = user.name

    return user
        
