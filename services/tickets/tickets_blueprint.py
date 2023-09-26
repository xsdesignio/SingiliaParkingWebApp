from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from auth.controllers.login import login_required
from datetime import datetime, timedelta

from decimal import Decimal

from services.users.controllers.withheld import add_withheld_to_user
from .models.ticket_model import TicketModel
from .models.available_tickets_model import AvailableTicketsModel
from .entities.available_ticket import AvailableTicket
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

    print("Query values: ", query_values)
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

    if payment_method == PaymentMethod.CASH:
        add_withheld_to_user(responsible, ticket_json['price'])

    created_at = ticket_json.get('created_at', datetime.now().strftime("%Y-%m-%d %H:%M"))

    created_at = ensure_date_format(created_at)

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


def ensure_date_format(date: str) -> str:
    correct_date = datetime.strptime(date)
    return correct_date.strftime("%Y-%m-%d %H:%M")


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



""" ------------------------ AVAILABLE ZONES ------------------------ """

@tickets_bp.get('/available-tickets')
@login_required
def available_tickets_page():
    available_tickets: list(AvailableTicket)
    available_tickets = AvailableTicketsModel.get_available_tickets()
    print("available tickets:", available_tickets)
    return render_template('available-tickets.html', available_tickets = available_tickets);



@tickets_bp.post('/available-tickets/create')
@login_required
def create_available_ticket():
    # get request infor from post form
    request_info = request.form
    ticket_duration = request_info.get('duration')
    ticket_price = Decimal(request_info.get('price'))

    if ticket_duration == None or ticket_price == None:
        flash('No se ha podido crear un nuevo modelo de ticket.', 'error')
        return redirect(url_for('tickets.available_tickets_page')), 301
    
    print("ticket duration and price")
    print(ticket_duration, ticket_price)
    
    try:
        ticket = AvailableTicketsModel.create_available_ticket(ticket_duration, float(ticket_price))
    except Exception as e:
        print("create_available_ticket: ", e)
        flash('No se ha podido crear un nuevo modelo de ticket.', 'error')
        return redirect(url_for('tickets.available_tickets_page')), 301
    
    if ticket == None:
        flash('No se ha podido crear un nuevo modelo de ticket.', 'error')
        return redirect(url_for('tickets.available_tickets_page')), 301

    print("ticket: ", ticket)
    flash('El ticket ha sido creado con éxito', 'success')
    return redirect(url_for('tickets.available_tickets_page')), 301
