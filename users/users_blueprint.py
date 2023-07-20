from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from users.models.user_model import UserModel
from auth.controllers.login import role_required




users_bp = Blueprint('users', __name__, url_prefix='/users', template_folder='./templates')



@role_required('ADMIN')
@users_bp.get('/')
def users_page():
    users = UserModel.get_users_list()
    return render_template('users.html', users=users)



@role_required('ADMIN')
@users_bp.get('/user/<id>')
def user_details(id):
    user = UserModel.get_user(id)
    if user != None:
        return render_template('user-details.html', user=user)
    else:
        return {'message': 'Ha ocurrido un error obteniendo el usuario.'}, 500


@role_required('ADMIN')
@users_bp.get('/get-user/<id>')
def get_user(id):
    user = UserModel.get_user(id)
    if user != None:
        return jsonify(user.to_json())
    else:
        return {'message': 'Ha ocurrido un error obteniendo el usuario.'}, 500



@role_required('ADMIN')
@users_bp.get('/get-users')
def get_users():
    users = UserModel.get_users_list()
    if users != None:
        return jsonify(users), 200
    else:
        return {'message': 'Ha ocurrido un error obteniendo los usuarios.'}, 500


@role_required('ADMIN')
@users_bp.post('/update-user')
def update_user():
    new_user_data: dict = request.get_json()
    updated_user = UserModel.update_user(new_user_data)
    
    if update_user != None:
        return jsonify(updated_user.to_json()), 200
    else:
        return {'message': 'Ha ocurrido un error actualizando el usuario.'}, 500


@role_required('ADMIN')
@users_bp.get('/create')
def create_get():
    return render_template('user-creation.html')


@role_required('ADMIN')
@users_bp.post('/create-user')
def create_user():
    
    user = UserModel.create_user(request.form['role'], request.form['name'], request.form['email'], request.form['password'])

    if update_user != None:
        return redirect(f"/users/user/{str(user.id)}", code=302)
    else:
        return {'message': 'Ha ocurrido un error creando el usuario.'}, 500

