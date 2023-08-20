from datetime import datetime

from .zones.entities.zone import Zone
from .tickets.controllers.tickets_controller import get_tickets_attributes_count
from .bulletins.controllers.bulletins_controller import get_bulletins_attributes_count



def get_resume_information(start_date: datetime = None, end_date: datetime = None, zone: Zone = None):
    """ Returns a dictionary with the resume information of the tickets and bulletins. """
    tickets_information = get_tickets_attributes_count(start_date, end_date, zone)
    bulletins_information = get_bulletins_attributes_count(start_date, end_date, zone)

    return {
        'tickets': tickets_information,
        'bulletins': bulletins_information
    }

