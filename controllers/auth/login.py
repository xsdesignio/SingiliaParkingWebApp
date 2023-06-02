from flask import redirect, request, session, url_for
from models.user_model import UserModel

from entities.user import User


 
def login_required(function):
    def wrapper(*args, **kwargs):
        if 'name' not in session:
            return redirect('/auth/login')
        return function(*args, **kwargs)
    return wrapper


def role_required(role:str):
    def decorator(function):
        def wrapper(*args, **kwargs):
            if 'name' not in session or session['role'] != role.upper():
                return redirect('/auth/login')
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
        session['role'] = user.role.name
        session['email'] = user.email
        session['name'] = user.name

    return user
        
