import re
from flask import Blueprint, flash, send_file, render_template, request, jsonify, redirect, url_for, after_this_request
from services.bulletins.controllers.bulletins_controller import get_bulletins_attributes_count

from services.tickets.controllers.tickets_controller import get_tickets_attributes_count
from services.utils.data_management import parse_date
from services.utils.reports.generation import create_report_for_zone
from .models.zone_model import ZoneModel
from .entities.zone import Zone
from auth.controllers.login import role_required

from services.bulletins.controllers.bulletins_controller import get_bulletins_attributes_count
from services.tickets.controllers.tickets_controller import get_tickets_attributes_count

from services.bulletins.models.bulletin_model import BulletinModel
from services.bulletins.entities.bulletin import Bulletin
from services.tickets.models.ticket_model import TicketModel
from services.tickets.entities.ticket import Ticket

from datetime import datetime, timedelta

import os



zones_bp = Blueprint('zones', __name__, url_prefix='/zones', template_folder='./templates')


@role_required('ADMIN')
@zones_bp.get('/')
def zones_page():
    zones = ZoneModel.get_zones_list()
    return render_template('zones.html', zones=zones)


@role_required('ADMIN')
@zones_bp.get('/zone/<id>')
def zone_details(id):
    zone = ZoneModel.get_zone(id)

    start_date = parse_date(request.args.get('start_date'), datetime.now() - timedelta(days=30))
    end_date = parse_date(request.args.get('end_date'), datetime.now())

    tickets_data = get_tickets_attributes_count(start_date, end_date, zone)
    bulletins_data = get_bulletins_attributes_count(start_date, end_date, zone)

    zones = ZoneModel.get_zones_list()

    start_date = start_date.strftime('%d-%m-%Y')
    end_date = end_date.strftime('%d-%m-%Y')

    if zone != None:
        return render_template('zone-details.html', zone=zone, zones=zones,  start_date = start_date, end_date = end_date, tickets_data=tickets_data, bulletins_data=bulletins_data)
    else:
        error_message = 'Ha ocurrido un error obteniendo la zona indicada, o esta no existe'
        return render_template('zone-details.html', error=error_message)
        



@role_required('ADMIN')
@zones_bp.get('/zone/<id>/edit')
def zone_editing_view(id):
    zone = ZoneModel.get_zone(id)

    return render_template('zone-editing.html', zone=zone)


@role_required('ADMIN')
@zones_bp.post('/zone/<id>/edit')
def zone_editing(id):
    zone = ZoneModel.get_zone(id)
    if zone != None:
        new_name = request.form.get('name')
        if new_name != None:
            ZoneModel.update_zone(id, new_name)
            flash('Zona actualizada correctamente', 'success')
            return redirect(url_for('zones.zone_details', id=id))

        

@role_required('ADMIN')
@zones_bp.get('/get-zone/<id>')
def get_zone(id: int):
    zone = ZoneModel.get_zone(id)
    if zone != None:
        return jsonify(zone.to_json()), 200
    else:
        return {'message': 'Ha ocurrido un error obteniendo la zona indicada'}, 500



@role_required('ADMIN')
@zones_bp.get('/get-available-zones/')
def get_available_zones():
    zones = ZoneModel.get_zones_list()

    if zones != None:
        return jsonify(zones), 200
    else:
        return {'message': 'Ha ocurrido un error obteniendo las zonas disponibles'}, 500
    


@role_required('ADMIN')
@zones_bp.get('/create')
def create_zone_page():
    return render_template('zone-creation.html')


@role_required('ADMIN')
@zones_bp.get('/zone/<id>/generate-report')
def generate_report(id):
    """ Returns the tickets filtered by date or by zone. Filters are optional and can be combined. They are obtained by get arguments."""
    report_object = request.args.get('report_object')

    start_date = parse_date(request.args.get('start_date'), datetime.now() - timedelta(days=30))
    end_date = parse_date(request.args.get('end_date'), datetime.now())

    zone = ZoneModel.get_zone(id)
    
    data: dict = {}
    if report_object == 'Tickets' or report_object == 'Both':
        #tickets = TicketModel.get_tickets(**query_values)
        tickets_amount_by_data = get_tickets_attributes_count(start_date=start_date, end_date=end_date, zone=zone)
        data["tickets"] = tickets_amount_by_data

    if report_object == 'Bulletins' or report_object == 'Both':
        #bulletins = BulletinModel.get_bulletins(**query_values)
        bulletins_amount_by_data = get_bulletins_attributes_count(start_date=start_date, end_date=end_date, zone=zone)
        data["bulletins"] = bulletins_amount_by_data
    

    created_report_url = create_report_for_zone(data, zone, start_date, end_date)

    @after_this_request
    def remove_file(response):
        os.remove(created_report_url)
        return response
    
    return send_file(created_report_url, as_attachment=True)


@role_required('ADMIN')
@zones_bp.post('/create-zone')
def create_zone():
    name = request.form['name']
    identifier = request.form['identifier']

    identifier_pattern = r'^[a-zA-Z]{2}$'

    if not re.match(identifier_pattern, identifier):
        flash('El identificador no es correcto, debe estar compuesto de 2 letras', 'error')
        return redirect(url_for('zones.create_zone_page'))

    zone: Zone = ZoneModel.create_zone(name, identifier)

    if zone != None:
        flash('Zona creada correctamente', 'success')
        return redirect(url_for('zones.zones_page'))
    else:
        flash('Ha ocurrido un error creando la zona', 'error')
        return redirect(url_for('zones.create_zone_page'))


@role_required('ADMIN')
@zones_bp.get('/delete/<id>')
def delete_zone(id):
    zone_deleted = ZoneModel.delete_zone(id)
    if zone_deleted:
        flash('Zona eliminada correctamente', 'success')
        return redirect(url_for('zones.zones_page'))
    
    flash('Ha ocurrido un error eliminando la zona', 'error')
    return redirect(url_for('zones.zone_details', id=id))



""" @role_required('ADMIN')
@zones_bp.get('/get-zone-responsibles')
def get_zone_responsibles():
    zones = ZoneModel.get_zones_list()
    if zones != None:
        return jsonify(zones), 200
    else:
        return {'message': 'Ha ocurrido un error obteniendo las zonas.'}, 500 """