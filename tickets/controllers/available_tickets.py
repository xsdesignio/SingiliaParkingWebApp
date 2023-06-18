from ..entities import Ticket, Zone
from enum import Enum


class AvailableTickets(Enum):
    tickets: dict = {
        "YELLOW": {
            'price': 70,
            'duration': 30 # minutes
        },
        "GREEN": {
            'price': 90,
            'duration': 60 # minutes = 1 hours
        },
        "ORANGE": {
            'price': 140,
            'duration': 90 # minutes
        },
        "RED": {
            'price': 180,
            'duration': 120 # minutes 
        }
    }

