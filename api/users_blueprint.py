from flask import Blueprint, request, jsonify
from models.user_model import UserModel
from controllers.auth.login import role_required

users_bp = Blueprint('users', __name__, url_prefix='/users')



@role_required('ADMIN')
@users_bp.get('/get-user/<id>')
def get_user(id):
    user = UserModel.get_user(id)
    if user != None:
        return jsonify(user.to_JSON())
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
        return jsonify(updated_user.to_JSON()), 200
    else:
        return {'message': 'Ha ocurrido un error actualizando el usuario.'}, 500


@role_required('ADMIN')
@users_bp.get('/create-user')
def create_user():
    user_data: dict = request.get_json()
    user = UserModel.create_user(user_data['role'], user_data['name'], user_data['email'], user_data['password'])
    
    if update_user != None:
        return jsonify(user.to_JSON()), 200
    else:
        return {'message': 'Ha ocurrido un error creando el usuario.'}, 500
