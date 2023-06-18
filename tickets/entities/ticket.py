from datetime import datetime
from decimal import Decimal
from users.entities.user import User

from .zone import Zone


class Ticket:
    id: int
    responsible: User
    duration: int # in minutes
    price: Decimal
    registration: str
    paid: bool
    zone: Zone
    created_at: datetime #  hour, minute, second, microsecond and timezone info as datetime params

    def __init__(self, 
                 id: int,
                 responsible:User, 
                 duration: int, 
                 price:float, 
                 registration:str,
                 paid:bool,
                 zone: Zone, 
                 created_at:datetime):
        self.id = id
        self.responsible = responsible
        self.duration = duration #minutes
        self.registration = registration
        self.price = Decimal(price)
        self.paid = paid
        self.zone = zone
        self.created_at = created_at
    

    def to_json(self):
        return {
            'id': self.id,
            'responsible': self.responsible.name,
            'duration': self.duration,
            'price': self.price,
            'registration': self.registration,
            'paid': self.paid,
            'zone': self.zone.name,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M")
        }
    
