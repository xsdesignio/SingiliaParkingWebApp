from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from zones.models.zone_model import ZoneModel
from auth.controllers.login import role_required




zones_bp = Blueprint('zones', __name__, url_prefix='/zones', template_folder='./templates')



@role_required('ADMIN')
@zones_bp.get('/')
def users_page():
    zones = ZoneModel.get_zones_list()
    return render_template('zones.html', users=zones)

