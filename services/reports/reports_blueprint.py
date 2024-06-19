import os
from flask import Blueprint, request, after_this_request, send_file, render_template, flash, session
from auth.controllers.login import role_required
from services.bulletins.controllers.bulletins_controller import get_bulletins_attributes_count
from services.zones.entities.zone import Zone
from services.zones.models.zone_model import ZoneModel
from .controllers.generation import create_report
from services.tickets.controllers.tickets_controller import get_tickets_attributes_count
from services.users.models.user_model import UserModel
from services.utils.data_management import parse_date
from datetime import datetime, timedelta


reports_bp = Blueprint('reports', __name__, url_prefix="/reports", template_folder="./templates")

@role_required('ADMIN')
@reports_bp.get('/')
def generate_report_view():
    users = UserModel.get_users_list()
    zones = ZoneModel.get_zones_list()
    return render_template('reports.html', users=users, zones=zones)



@role_required('ADMIN')
@reports_bp.post('/generate-report')
def generate_report():
    """ Returns the tickets filtered by date or by zone. Filters are optional and can be combined. They are obtained by get arguments."""
    
    start_date = parse_date(request.form.get('start_date'), datetime.now() - timedelta(days=30))
    end_date = parse_date(request.form.get('end_date'), datetime.now())
    user = request.form.get('user_name') 
    user = None if not user else UserModel.get_user_by_name(user)

    zone_name = request.form.get('zone_name')
    zone_name = zone_name if zone_name != "ALL" else None
    zone = None if not zone_name else ZoneModel.get_zone_by_name(zone_name)


    params = {'start_date': start_date, 'end_date': end_date}

    if zone is not None:
        params['zone'] = zone
    if user is not None:
        params['user'] = user

    data: dict = {}
    data["tickets"] = get_tickets_attributes_count(**params)
    data["bulletins"] = get_bulletins_attributes_count(**params)
    
    report_url = create_report(data, user, zone, start_date, end_date)

    @after_this_request
    def remove_file(response):
        # Remove the report from the website once downloaded by the user
        os.remove(report_url)
        return response
    
    return send_file(report_url, as_attachment=True)
    
