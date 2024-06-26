from flask import redirect, request, session, url_for, jsonify
from functools import wraps
from services.users.models.user_model import UserModel

from services.users.entities.user import User


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if 'name' not in session:
            redirect_url = url_for('auth.login_page')
            return redirect(redirect_url), 301
        return function(*args, **kwargs)
    return wrapper


# Create the enum for the roles so the decorator can check if the user has the required role or a higher one

def role_required(role:str):
    def decorator(function):
        def wrapper(*args, **kwargs):
            if 'name' not in session:
                redirect_url = url_for('auth.login_page')
                return redirect(redirect_url)
            
            if 'role' not in session:
                redirect_url = url_for('auth.login_page')
                return redirect(redirect_url)

        
            session_role = session['role']
            role = role.upper()
            if role == 'EMPLOYEE':
                if session_role != role and session_role != 'MANAGER' and session_role != 'ADMIN':
                    return {}, 500
                
            elif role == 'MANAGER':
                if session_role != role and session_role != 'ADMIN':
                    return {}, 500
            
            elif role == 'ADMIN':
                if session_role != role:
                    return {}, 500
                
            if session['role'] != role.upper():
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

        if user.associated_zone != None:
            session['associated_zone'] = user.associated_zone.name


    return user
        
