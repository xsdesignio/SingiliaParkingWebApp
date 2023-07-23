from flask import Blueprint, render_template, request, jsonify, session
from auth.controllers.login import login_required

from .models.ticket_model import TicketModel
from .entities.ticket import Ticket
from datetime import datetime, timedelta

from .controllers.ticket_controller import get_tickets_attributes_count


tickets_bp = Blueprint('tickets', __name__, url_prefix='/tickets', template_folder='./templates')


@tickets_bp.get('/')
@login_required
def tickets_page():
    """ Returns the tickets filtered by date or by zone. Filters are optional and can be combined. They are obtained by get arguments."""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    zone = request.args.get('zone')

    if end_date is not None and end_date != '':
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    else:
        end_date = datetime.now()

    if start_date is not None and start_date != '':
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
    else:
        start_date = datetime.now() - timedelta(days=30)

    if zone == 'all':
        zone = None

    tickets = TicketModel.get_tickets_by_filter(start_date, end_date, zone)

    all_tickets_count = get_tickets_attributes_count(start_date, end_date, zone)

    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')

    return render_template('tickets.html', tickets = tickets, start_date = start_date, end_date = end_date, zone = zone, tickets_data = all_tickets_count)



@tickets_bp.get('/get-ticket/<id>')
@login_required
def get_ticket(id: int):
    ticket = TicketModel.get_ticket(id)
    if ticket != None:
        return jsonify(ticket.to_json()), 200
    else:
        return {'message': 'Ha ocurrido un error obteniendo el ticket indicado'}, 500


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
    ticket_json = request.get_json()
    ticket: Ticket

    responsible_id = ticket_json.get('responsible_id', session["id"])

    created_at = ticket_json.get('created_at', datetime.now().strftime("%Y-%m-%d %H:%M"))

    try:
        ticket = TicketModel.create_ticket(
            responsible_id, 
            ticket_json['duration'], 
            ticket_json['registration'], 
            ticket_json['price'], 
            ticket_json["paid"], 
            ticket_json['location'],
            created_at)
    except Exception as e:
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
        print(exception)
        return jsonify({'message': exception.__str__()}), 400



