from flask import Blueprint, flash, render_template, request, jsonify, redirect, send_file
from .models.user_model import UserModel
from auth.controllers.login import role_required
from datetime import datetime, timedelta

from services.tickets.models.ticket_model import TicketModel
from services.tickets.controllers.tickets_controller import get_tickets_attributes_count
from services.bulletins.controllers.bulletins_controller import get_bulletins_attributes_count
from services.bulletins.models.bulletin_model import BulletinModel
from services.zones.models.zone_model import ZoneModel
from services.users.entities.user import User
from services.utils.reports.generation import create_report_for_user 



users_bp = Blueprint('users', __name__, url_prefix='/users', template_folder='./templates')



@role_required('ADMIN')
@users_bp.get('/')
def users_page():
    users = UserModel.get_users_list()
    return render_template('users.html', users=users)


@role_required('ADMIN')
@users_bp.get('/user/<id>/generate-report')
def generate_report(id):
    """ Returns the tickets filtered by date or by zone. Filters are optional and can be combined. They are obtained by get arguments."""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    request_zone = request.args.get('zone')


    if end_date is not None and end_date != '':
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    else:
        end_date = datetime.now()

    if start_date is not None and start_date != '':
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    else:
        start_date = datetime.now() - timedelta(days=30)

    user = UserModel.get_user(id)
    query_values = {
        "start_date": start_date, 
        "end_date":  end_date, 
        "responsible_id": user.id
    }

    if not (request_zone == 'all' or request_zone == None):
        zone = ZoneModel.get_zone_by_name(request_zone)
        if zone != None:
            query_values["zone_id"] = zone.id

    #tickets = TicketModel.get_tickets(**query_values)
    tickets_amount_by_data = get_tickets_attributes_count()
    bulletins_amount_by_data = get_bulletins_attributes_count()

    data = {
        "tickets":tickets_amount_by_data,
        "bulletins":bulletins_amount_by_data
    }

    created_report_url = create_report_for_user(data, user, start_date, end_date)

    return send_file(created_report_url, as_attachment=True)


@role_required('ADMIN')
@users_bp.get('/user/<id>')
def user_details(id):
    user: User = UserModel.get_user(id)

    query_values = {
        "responsible_id": user.id
    }

    tickets_data = get_tickets_attributes_count(user = user)

    bulletins_data = get_bulletins_attributes_count(user = user)

    available_zones = ZoneModel.get_zones_list()


    if user != None:
        return render_template('user-details.html', user=user, tickets_data=tickets_data, bulletins_data=bulletins_data, zones=available_zones)
    else:
        return {'message': 'Ha ocurrido un error obteniendo el usuario.'}, 500



@role_required('ADMIN')
@users_bp.post('/user/<id>/assign-zone/')
def asign_zone(id):
    user: User = UserModel.get_user(id)
    zone_name = request.form.get('zone')

    if user != None:
        zone = ZoneModel.get_zone_by_name(zone_name)
        if zone != None:
            user.zone_id = zone.id
            zone_assigned = UserModel.asign_zone_to_user(user.id, zone)
            if zone_assigned:
                flash('Zona asignada correctamente.', 'success')
                return redirect(f"/users/user/{str(user.id)}", code=302)
            else:
                flash('Ha ocurrido un error desconocido asignando la zona.', 'error')
                return redirect(f"/users/user/{str(user.id)}", code=302)
        else:
            flash('La zona introducida no existe.', 'error')
            return redirect(f"/users/user/{str(user.id)}", code=302)
    else:
        flash('Ha ocurrido un error obteniendo el usuario.', 'error')
        return redirect('/users', code=302)


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
@users_bp.post('user/<id>/delete')
def delete_user(id):
    deleted_user = UserModel.delete_user(id)
    if deleted_user != None:
        flash('Usuario eliminado correctamente.', 'success')
        return redirect('/users', code=302)
        # return jsonify(deleted_user.to_json()), 200
    else:
        return {'message': 'Ha ocurrido un error eliminando el usuario.'}, 500




@role_required('ADMIN')
@users_bp.get('/create')
def create_get():
    return render_template('user-creation.html')


@role_required('ADMIN')
@users_bp.post('/create-user')
def create_user():
    
    user = UserModel.create_user(request.form['role'], request.form['name'], request.form['email'], request.form['password'])

    if user != None and user.id != None:
        flash('Usuario creado correctamente.', 'success')
        return redirect(f"/users/user/{str(user.id)}", code=302)
    else:
        flash('Los datos introducidos no son correctos.', 'error')
        return redirect('/users/create', code=302)

