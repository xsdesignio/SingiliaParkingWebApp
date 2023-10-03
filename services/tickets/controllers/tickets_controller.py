from services.zones.models.zone_model import ZoneModel
from services.zones.entities.zone import Zone
from services.users.entities.user import User
from ..models.ticket_model import TicketModel
from datetime import datetime
from decimal import Decimal

from ..models.available_ticket_model import AvailableTicketModel



def get_tickets_attributes_count(start_date: datetime = None, end_date: datetime = None, zone: Zone = None, user: User = None):
    """Return a dictionary with the variables and their count"""
    
    query_dict = {}

    available_tickets: list[dict] = AvailableTicketModel.get_available_tickets()
    
    if start_date:
        query_dict["start_date"] = start_date

    if end_date:
        query_dict["end_date"] = end_date

    if(zone):
        query_dict["zone_id"] = zone.id

    if(user):
        query_dict["responsible_id"] = user.id

    paid_by_card = TicketModel.count_tickets(**query_dict, payment_method = "CARD")
    paid_by_cash = TicketModel.count_tickets(**query_dict, payment_method = "CASH")


    tickets_amount = {
        "tickets_amount": paid_by_card + paid_by_cash,
        "paid_by_card": paid_by_card,
        "paid_by_cash": paid_by_cash,
        "data_by_duration": [],
        "total_income": Decimal("0.00")
    }

    for available_ticket in available_tickets:
        duration = available_ticket["duration"]
        price = available_ticket["price"]
        count_by_duration = TicketModel.count_tickets(**query_dict, duration = duration)
        
        paid_by_card = TicketModel.count_tickets(**query_dict, duration = duration, payment_method = "CARD")
        paid_by_cash = TicketModel.count_tickets(**query_dict, duration = duration, payment_method = "CASH")

        data_by_duration_dict = {
            "duration": duration,
            "amount": count_by_duration,
            "paid_by_card": paid_by_card,
            "paid_by_cash": paid_by_cash,
            "total_income": count_by_duration * price,
        }

        tickets_amount["data_by_duration"].append(data_by_duration_dict)

        tickets_amount["total_income"] += data_by_duration_dict["total_income"]

    return tickets_amount

