from datetime import datetime
from entities.user import User, UserRole

from .zone import Zone


class Ticket:
    id: int
    responsible: User
    created_at: datetime #  hour, minute, second, microsecond and timezone info as datetime params
    duration: int # in minutes
    zone: Zone

    def __init__(self, responsible:User, duration: int, zone: Zone, created_at:datetime):
        self.id = id
        self.responsible = responsible
        self.duration = duration
        self.zone = zone
        self.created_at = created_at
    

    def to_Json(self):
        return {
            'id': self.id,
            'responsible': self.responsible.name,
            'date': self.datetime,
            'zone': self.zone.name
        }
    
