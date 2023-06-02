from flask import Blueprint, request, jsonify
from controllers.auth.login import login_required

from models.ticket_model import TicketModel
import datetime


tickets_bp = Blueprint('tickets', __name__, url_prefix='/tickets')



@login_required
@tickets_bp.get('/get-ticket')
def get_ticket():
    ticket = TicketModel.get_ticket()
    if ticket != None:
        return jsonify(ticket.to_JSON), 200
    else:
        return {'message': 'Ha ocurrido un error obteniendo el ticket indicado'}, 500


@login_required
@tickets_bp.get('/get-tickets')
def get_tickets():
    tickets_json = TicketModel.get_tickets_JSON()
    if tickets_json != None:
        return jsonify(tickets_json), 200
    else:
        return {'message': 'Ha ocurrido un error obteniendo los tickets, initéntelo de nuevo más tarde'}, 500



@login_required
@tickets_bp.post('/create-ticket/')
def create_ticket():
    ticket_json = request.get_json()
    ticket = TicketModel.create_ticket(ticket_json['author'], ticket_json['zone'], datetime.datetime.now)
    if ticket != None:
        return jsonify(ticket.toString), 200
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