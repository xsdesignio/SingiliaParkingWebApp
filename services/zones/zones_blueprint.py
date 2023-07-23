from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from .models.zone_model import ZoneModel
from .entities.zone import Zone
from auth.controllers.login import role_required


zones_bp = Blueprint('zones', __name__, url_prefix='/zones', template_folder='./templates')


@role_required('ADMIN')
@zones_bp.get('/')
def zones_page():
    zones = ZoneModel.get_zones_list()
    print(f"zones: {zones}")
    return render_template('zones.html', zones=zones)


@role_required('ADMIN')
@zones_bp.get('/zone/<id>')
def zone_details(id):
    zone = ZoneModel.get_zone(id)
    if zone != None:
        return render_template('zone-details.html', zone=zone)
    else:
        error_message = 'Ha ocurrido un error obteniendo la zona indicada, o esta no existe'
        return render_template('zone-details.html', error=error_message)
        

@role_required('ADMIN')
@zones_bp.get('/get-zone/<id>')
def get_zone(id: int):
    zone = ZoneModel.get_zone(id)
    if zone != None:
        return jsonify(zone.to_json()), 200
    else:
        return {'message': 'Ha ocurrido un error obteniendo la zona indicada'}, 500


@role_required('ADMIN')
@zones_bp.get('/create')
def create_zone_page():
    return render_template('zone-creation.html')



@role_required('ADMIN')
@zones_bp.post('/create-zone')
def create_zone():
    name = request.form['name']

    print(f"name: {name}")
    zone: Zone = ZoneModel.create_zone(name)

    print(f"zone: {zone.__str__()}")

    if zone != None:
        return redirect(url_for('zones.zones_page'))
    else:
        return redirect(url_for('zones.create_zone_page'))


@role_required('ADMIN')
@zones_bp.post('/delete')
def delete_zone():
    id = request.form['id']
    ZoneModel.delete_zone(id)
    return redirect(url_for('zones.zones_page'))