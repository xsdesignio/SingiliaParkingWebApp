
from ..models.ticket_model import TicketModel
from datetime import datetime



def get_tickets_attributes_count(start_date: datetime = None, end_date: datetime = None, location: str = None):
    """Return a dictionary with the variables and their count"""
    paid_by_card = TicketModel.count_tickets_variable_by_filter(start_date, end_date, location, 'paid', True)
    paid_by_cash = TicketModel.count_tickets_variable_by_filter(start_date, end_date, location, 'paid', False)
    duration_of_30 = TicketModel.count_tickets_variable_by_filter(start_date, end_date, location, 'duration', 30)
    duration_of_60 = TicketModel.count_tickets_variable_by_filter(start_date, end_date, location, 'duration', 60)
    duration_of_90 = TicketModel.count_tickets_variable_by_filter(start_date, end_date, location, 'duration', 90)
    duration_of_120 = TicketModel.count_tickets_variable_by_filter(start_date, end_date, location, 'duration', 120)

    tickets_amount_by_data = {
        "paid_by_card": paid_by_card,
        "paid_by_cash": paid_by_cash,
        "duration_of_30": duration_of_30,
        "duration_of_60": duration_of_60,
        "duration_of_90": duration_of_90,
        "duration_of_120": duration_of_120,
    }

    return tickets_amount_by_data