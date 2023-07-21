from flask import Blueprint, render_template, send_from_directory, request, redirect, url_for, jsonify
from flask import session, make_response
from .controllers.login import login_user, login_required
from .controllers.signup import signup_user

from services.users.entities.user import User



auth_bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='./templates')


@auth_bp.get('/login')
def login_page():
    """Login page"""
    if 'id' in session:
        return redirect('/')
    return render_template('login.html')


@auth_bp.post('/login')
def login():
    """Login user by a json request and return user data if login is successful
    
    Return: user data
    """
    
    data = request.get_json()
    email = data['email']
    password = data['password']

    # Loggin user. Get true or false depending on whether login is made successfully
    logged_in_user: User = login_user(email, password)
        
    if(logged_in_user != None):
        return {
            "id": logged_in_user.id,
            "role": logged_in_user.role.value,
            "name": logged_in_user.name,
            "email": logged_in_user.email,
        }, 200
    else:
        return jsonify({
            "message": "Data introduced isn't correct"
        }), 500


@auth_bp.post('/signup')
def signup():
    """Signup user by a json request and return user data if signup is successful

    Return: user data
    """

    data = request.get_json()

    role = data['role']
    name = data['name']
    email = data['email']
    password = data['password']

    secret_code = data['secret_code']

    if secret_code != 4578:
        return(jsonify({
            "message": "You need the secret code to create an account"
        })), 500

    # Signup user. Get true or false depending on whether login is made successfully
    signed_up_user = signup_user(role, name, email, password)


    if signed_up_user != None:
        return jsonify({
            "id": signed_up_user.id,
            "role": signed_up_user.role.value,
            "name": data['name'],
            "email": signed_up_user.email,
        }), 200
    else:
        return jsonify({
            "message": "Data introduced isn't correct"
        }), 500


@auth_bp.get('/logout')
def logout():
    """Logout user by clearing session"""
    session.clear()
        
    return {"message": "Se ha cerrado sesion correctamente"}, 200



@login_required
@auth_bp.get('/session')
def get_session():
    """
    Get session data

    Return: session data (user info)
    """
    session_data: dict[int, str, str, str] = {}
    
    if 'username' in session:
        session_data = {
            "id": session['id'],
            "role": session['role'],
            "name": session['name'],
            "email": session['email']
        }
    else:
        return jsonify({"ERROR": "There is no session active"}), 500
    
    session_data = jsonify(session_data)
    return session_data, 200


    
@auth_bp.get('/clear-session')
def clear_session():
    session.clear()
    return 200

