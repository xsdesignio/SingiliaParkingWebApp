from flask import Blueprint, render_template, request, jsonify, session
from auth.controllers.login import login_required
from datetime import datetime, timedelta
from .models.ticket_model import TicketModel
from .entities.ticket import Ticket
from services.users.models.user_model import UserModel
from services.zones.entities.zone import Zone
from services.zones.models.zone_model import ZoneModel

from .controllers.tickets_controller import get_tickets_attributes_count

from services.utils.payment_methods import PaymentMethod
from services.utils.data_management import parse_date, get_queries_from_request_data, get_range_from_page

tickets_bp = Blueprint('tickets', __name__, url_prefix='/tickets', template_folder='./templates')


@tickets_bp.get('/')
@login_required
def tickets_page():
    """ Returns the tickets filtered by date or by zone. Filters are optional and can be combined. They are obtained by get arguments."""

    start_date = parse_date(request.args.get('start_date'), datetime.now() - timedelta(days=30))
    end_date = parse_date(request.args.get('end_date'), datetime.now())
    

    all_tickets_count: dict
    request_zone = request.args.get('zone', 'all')

    zone = None
    if request_zone != 'all':
        zone = ZoneModel.get_zone_by_name(request_zone)

    all_tickets_count = get_tickets_attributes_count(start_date, end_date, zone)

    # Convert dates to string in order to pass them to the template
    start_date = start_date.strftime('%d-%m-%Y')
    end_date = end_date.strftime('%d-%m-%Y')
    zones = ZoneModel.get_zones_list()

    return render_template('tickets.html', start_date = start_date, end_date = end_date, tickets_data = all_tickets_count, available_zones = zones, zone = zone)



@tickets_bp.get('/get-ticket/<id>')
@login_required
def get_ticket(id: int):
    ticket = TicketModel.get_ticket(id)
    if ticket != None:
        return jsonify(ticket.to_json()), 200
    else:
        return {'message': 'Ha ocurrido un error obteniendo el ticket indicado'}, 500



@tickets_bp.post('/get-tickets/<page>')
@login_required
def get_tickets_by_page(page = 0):

    # Getting and preparing the data
    tickets_range = get_range_from_page(int(page))

    query_values = None

    if(request.content_type == 'application/json') and (request.json != None):
        query_values = get_queries_from_request_data(request.json)

    # Get tickets from database
    tickets_json = TicketModel.get_tickets(tickets_range, **query_values)

    # Return the tickets as JSON
    if tickets_json is not None:
        return jsonify(tickets_json), 200
    else:
        return jsonify({'message': 'Ha ocurrido un error obteniendo los tickets, inténtelo de nuevo más tarde'}), 500



@tickets_bp.get('/get-tickets')
@login_required
def get_tickets():
    tickets_json = TicketModel.get_tickets()
    if tickets_json != None:
        return jsonify(tickets_json), 200
    else:
        return jsonify({'message': 'Ha ocurrido un error obteniendo los tickets, initéntelo de nuevo más tarde'}), 500



 
@tickets_bp.post('/create/')
@login_required
def create_ticket():
    """ 
    Creates a ticket with the data provided in the request body in json format.
    
    """
    ticket_json = request.get_json()
    ticket: Ticket
    

    responsible_id = ticket_json.get('responsible_id', session["id"])
    responsible = UserModel.get_user(responsible_id)

    requested_zone: str = ticket_json.get('zone')

    if requested_zone == None:
        requested_zone = ticket_json.get('zone_name')

    zone = ZoneModel.get_zone_by_name(requested_zone)

    payment_method = PaymentMethod.get_enum_value(ticket_json['payment_method'])

    created_at = ticket_json.get('created_at', datetime.now().strftime("%Y-%m-%d %H:%M"))

    try:
        
        ticket = TicketModel.create_ticket(
            responsible = responsible, 
            zone = zone,
            duration = ticket_json['duration'], 
            registration = ticket_json['registration'], 
            price = ticket_json['price'], 
            payment_method = payment_method,
            paid = bool(ticket_json.get("paid", False)), 
            created_at = created_at
        )

    except Exception as e:
        print("create_ticket: ", e)
        return jsonify({'message': 'El ticket no pudo ser creado.'}), 400


    if ticket != None:
        ticket_data: dict = ticket.to_json()
        return jsonify(ticket_data), 200
    else:
        return {'message': 'El ticket no pudo ser creado.'}, 500



@tickets_bp.post('/pay/<id>')
@login_required
def pay_ticket(id: int):
    try:
        ticket_id = int(id)

        ticket = TicketModel.get_ticket(ticket_id)

        if(ticket == None):
            return jsonify({'message': "El ticket no existe"}), 400
        
        if(ticket.paid == True):
            return jsonify({'message': "El ticket introducido ya ha sido pagado"}), 400
         
        TicketModel.pay_ticket(ticket_id)

        return jsonify({'message': 'El ticket ha sido pagado con éxito'}), 200
    
    except Exception as exception:
        print("pay_ticket: ", exception)
        return jsonify({'message': exception.__str__()}), 400


