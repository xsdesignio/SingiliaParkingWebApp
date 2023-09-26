from services.zones.models.zone_model import ZoneModel
from services.zones.entities.zone import Zone
from services.users.entities.user import User
from ..models.ticket_model import TicketModel
from datetime import datetime
from decimal import Decimal



def get_tickets_attributes_count(start_date: datetime = None, end_date: datetime = None, zone: Zone = None, user: User = None):
    """Return a dictionary with the variables and their count"""
    
    query_dict = {}
    
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
    duration_of_30 = TicketModel.count_tickets(**query_dict, duration = 30)
    duration_of_60 = TicketModel.count_tickets(**query_dict, duration = 60)
    duration_of_90 = TicketModel.count_tickets(**query_dict, duration = 90)
    duration_of_120 = TicketModel.count_tickets(**query_dict, duration = 120)

    if paid_by_card is None:
        paid_by_card = 0
    if paid_by_cash is None:
        paid_by_cash = 0
        
    

    tickets_amount = {
        "tickets_amount": paid_by_card + paid_by_cash,
        "paid_by_card": paid_by_card,
        "paid_by_cash": paid_by_cash,
        "duration_of_30": duration_of_30,
        "total_income_by_30": duration_of_30 * get_prices_by_duration(30),
        "duration_of_60": duration_of_60,
        "total_income_by_60": duration_of_60 * get_prices_by_duration(60),
        "duration_of_90": duration_of_90,
        "total_income_by_90": duration_of_90 * get_prices_by_duration(90),
        "duration_of_120": duration_of_120,
        "total_income_by_120": duration_of_120 * get_prices_by_duration(120),
    }
    total_income = round(tickets_amount["total_income_by_30"] + tickets_amount["total_income_by_60"] + tickets_amount["total_income_by_90"] + tickets_amount["total_income_by_120"], 2)
    tickets_amount["total_income"] = total_income


    return tickets_amount




def get_prices_by_duration(duration):
    """Return a dictionary with the prices by duration"""
    
    if duration <= 30:
        return Decimal("0.70")
    elif duration <= 60:
        return Decimal("0.90")
    elif duration <= 90:
        return Decimal("1.40")
    elif duration <= 120:
        return Decimal("1.80")
    elif duration <= 180:
        return Decimal("3.60")
    elif duration <= 240:
        return Decimal("4.50")