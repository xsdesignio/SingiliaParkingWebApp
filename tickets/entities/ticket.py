from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from users.entities.user import User


@dataclass
class Ticket:
    id: int
    responsible: User
    duration: int # in minutes
    price: Decimal
    registration: str
    paid: bool
    location: str
    created_at: datetime #  hour, minute, second, microsecond and timezone info as datetime params

    def __post_init__(self):
        if not isinstance(self.price, Decimal):
            self.price = Decimal(self.price)
    

    def to_json(self):
        return {
            'id': self.id,
            'responsible': self.responsible.name,
            'duration': self.duration,
            'price': self.price,
            'registration': self.registration,
            'paid': self.paid,
            'location': self.location,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M")
        }
    
