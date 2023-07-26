from services.zones.models.zone_model import ZoneModel
from services.zones.entities.zone import Zone
from ..models.ticket_model import TicketModel
from datetime import datetime



def get_tickets_attributes_count(start_date: datetime = None, end_date: datetime = None, zone: Zone = None):
    """Return a dictionary with the variables and their count"""
    
    query_dict = {}
    
    if start_date:
        query_dict["start_date"] = start_date

    if end_date:
        query_dict["end_date"] = end_date

    if(zone):
        query_dict["zone_id"] = zone.id


    paid_by_card = TicketModel.count_tickets(**query_dict, payment_method = "CARD")
    paid_by_cash = TicketModel.count_tickets(**query_dict, payment_method = "CARD")
    duration_of_30 = TicketModel.count_tickets(**query_dict, duration = 30)
    duration_of_60 = TicketModel.count_tickets(**query_dict, duration = 60)
    duration_of_90 = TicketModel.count_tickets(**query_dict, duration = 90)
    duration_of_120 = TicketModel.count_tickets(**query_dict, duration = 120)

    if paid_by_card is None:
        paid_by_card = 0
    if paid_by_cash is None:
        paid_by_cash = 0
    

    tickets_amount_by_data = {
        "total_tickets": paid_by_card + paid_by_cash,
        "paid_by_card": paid_by_card,
        "paid_by_cash": paid_by_cash,
        "duration_of_30": duration_of_30,
        "duration_of_60": duration_of_60,
        "duration_of_90": duration_of_90,
        "duration_of_120": duration_of_120,
    }


    return tickets_amount_by_data