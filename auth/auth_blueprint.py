from flask import Blueprint, render_template, send_from_directory, request, redirect, url_for, jsonify
from flask import session, make_response
from .controllers.login import login_user, login_required
from .controllers.signup import signup_user

from services.users.entities.user import User

import os



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
        user_data = logged_in_user.to_json()
        return user_data, 200
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

    security_code_sent = data['security_code'] 

    security_code = os.environ.get('SECURITY_CODE')
    
    if security_code_sent != security_code:
        return(jsonify({
            "message": "You need the secret code to create an account"
        })), 500

    # Signup user. Get true or false depending on whether login is made successfully
    signed_up_user = signup_user(role, name, email, password)

    if signed_up_user != None:
        return signed_up_user.to_json(), 200
    else:
        return jsonify({
            "message": "Data introduced isn't correct"
        }), 500


@auth_bp.get('/logout')
def logout():
    """Logout user by clearing session"""
    session.clear()
        
    return redirect('/auth/login', code=302)



@login_required
@auth_bp.get('/session')
def get_session():
    """
    Get session data

    Return: session data (user info)
    """
    print("session: ", session)
    
    if 'name' not in session:  
        print("the error may be here")
        return jsonify({"ERROR": "There is no session active"}), 500
        

    session_data: dict[int, str, str, str, str] = {
        "id": session['id'],
        "role": session['role'],
        "name": session['name'],
        "email": session['email']
    }

    if 'associated_zone' in session:
        session_data['associated_zone'] = session['associated_zone']

    session_data = jsonify(session_data)
    print("session data jsonified: ", session_data)
    return session_data, 200


    
@auth_bp.get('/clear-session')
def clear_session():
    session.clear()
    return 200

