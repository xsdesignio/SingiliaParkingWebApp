from flask import Blueprint, render_template, request, after_this_request, send_file
from auth.controllers.login import login_required, role_required
from services.export.export_data import export_tickets
from services.export.export_data import export_bulletins
from services.export.file_extensions import FileExtensions
from services.users.entities.user import User
from services.utils.data_management import parse_date
from datetime import datetime, timedelta
from services.users.models.user_model import UserModel
from services.zones.models.zone_model import ZoneModel
from services.zones.entities.zone import Zone
from services.tickets.entities.ticket import Ticket
from services.tickets.models.ticket_model import TicketModel
from services.bulletins.entities.bulletin import Bulletin
from services.bulletins.models.bulletin_model import BulletinModel
from database.base_model import BaseModel
import os

export_bp = Blueprint('export', __name__, url_prefix='/export', template_folder='./templates')



@role_required('ADMIN')
@export_bp.get('/')
def export_page():
    
    users = UserModel.get_users_list()
    zones = ZoneModel.get_zones_list()

    return render_template('export.html', users=users, zones=zones)


@role_required('ADMIN')
@export_bp.post('/export-database-tickets')
def export_tickets_from_db():

    data: dict = request.form

    params = get_params()

    tickets: list = BaseModel.delete_elements('tickets', **params)


    print(len(tickets))
    extension = data.get("extension", "csv")
    
    if(extension == "xlsx"):
        extension = FileExtensions.XLSX
    else:
        extension = FileExtensions.CSV

    export_path: str = export_tickets(tickets, extension)

    @after_this_request
    def remove_file(response):
        # Remove the report from the website once downloaded by the user
        os.remove(export_path)
        return response

    return send_file(export_path, as_attachment=True)


@role_required('ADMIN')
@export_bp.post('/export-database-bulletins')
def export_bulletins_from_db():

    data: dict = request.form

    params = get_params()
    
    bulletins: list[Bulletin] = BaseModel.delete_elements('bulletins', **params)

    extension = data.get("extension", "csv")
    if(extension == "xlsx"):
        extension = FileExtensions.XLSX
    else:
        extension = FileExtensions.CSV

    export_path: str = export_bulletins(bulletins, extension)

    @after_this_request
    def remove_file(response):
        # Remove the report from the website once downloaded by the user
        os.remove(export_path)
        return response

    return send_file(export_path, as_attachment=True)




def get_params():
    data: dict = request.form

    # CHANGE SO START AND END_DATE FIELDS ARE REQUIRED
    start_date = parse_date(data.get('start_date'), datetime.now() - timedelta(days=30))
    end_date = parse_date(data.get('end_date'), datetime.now())

    user = request.form.get('user_name') 
    user: User = None if not user else UserModel.get_user_by_name(user)

    zone_name = data.get('zone_name') if data.get('zone_name') != "ALL" else None
    zone: Zone = None if not zone_name else ZoneModel.get_zone_by_name(zone_name)

    params = {'start_date': start_date, 'end_date': end_date}

    if zone is not None:
        params['zone_id'] = zone.id
    if user is not None:
        params['responsible_id'] = user.id
    
    return params

