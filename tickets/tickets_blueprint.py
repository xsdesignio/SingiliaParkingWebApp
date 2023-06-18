from flask import Blueprint, request, jsonify
from auth.controllers.login import login_required

from .models.ticket_model import TicketModel
from .entities.ticket import Ticket
import datetime


tickets_bp = Blueprint('tickets', __name__, url_prefix='/tickets')



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
        return {'message': 'Ha ocurrido un error obteniendo los tickets, initéntelo de nuevo más tarde'}, 500


 
@tickets_bp.post('/create/')
@login_required
def create_ticket():
    ticket_json = request.get_json()
    ticket: Ticket
    try:
        ticket = TicketModel.create_ticket(
            ticket_json['responsible_id'], 
            ticket_json['duration'], 
            ticket_json['registration'], 
            ticket_json['price'], 
            ticket_json["paid"], 
            ticket_json['zone_id'],
            ticket_json['created_at'])
    except Exception as e:
        return {'message': 'El ticket no pudo ser creado.'}, 400


    if ticket != None:
        ticket_data: dict = ticket.to_json()
        return jsonify(ticket_data), 200
    else:
        return {'message': 'El ticket no pudo ser creado.'}, 500





""" 
@tickets_bp.create('/create-tickets-bunch')
@login_required
def create_tickets_bunch():
    ticket_json = request.get_json()
    ticket = TicketModel.create_tickets_bunch(ticket_json['author'], ticket_json['zone'], datetime.datetime.now)
    if ticket != None:
        return ticket, 200
    else:
        return {'message': 'El ticket no pudo ser creado.'}, 500
"""