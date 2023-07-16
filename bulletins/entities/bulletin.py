from dataclasses import dataclass

from datetime import datetime
from decimal import Decimal
from users.entities.user import User



@dataclass
class Bulletin:
    id: int
    responsible: User
    location: str
    registration: str
    duration: int # in minutes
    price: Decimal
    paid: bool
    created_at: datetime #  hour, minute, second, microsecond and timezone info as datetime params

    # Optional
    brand: str = None
    model: str = None
    color: str = None



    def __post_init__(self):
        if not isinstance(self.price, Decimal):
            self.price = Decimal(self.price)


    def to_json(self):
        return {
            "id": self.id,
            "responsible": self.responsible.name,
            "location": self.location,
            "registration": self.registration,
            "duration": self.duration, #minutes
            "price": self.price,
            "paid": self.paid,
            "brand": self.brand,
            "model": self.model,
            "color": self.color,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M")
        }
    
