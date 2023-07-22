from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from .models.zone_model import ZoneModel
from auth.controllers.login import role_required




zones_bp = Blueprint('zones', __name__, url_prefix='/zones', template_folder='./templates')



@role_required('ADMIN')
@zones_bp.get('/')
def zones_page():
    zones = ZoneModel.get_zones_list()
    return render_template('zones.html', zones=zones)



@role_required('ADMIN')
@zones_bp.post('/create')
def create_zone():
    name = request.form['name']
    ZoneModel.create_zone(name)
    return redirect(url_for('zones.zones_page'))


@role_required('ADMIN')
@zones_bp.post('/delete')
def delete_zone():
    id = request.form['id']
    ZoneModel.delete_zone(id)
    return redirect(url_for('zones.zones_page'))