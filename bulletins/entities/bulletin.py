from datetime import datetime
from decimal import Decimal
from users.entities.user import User

class Bulletin:
    id: int
    responsible: User
    location: str
    registration: str
    duration: int # in minutes
    price: Decimal
    paid: bool
    brand: str
    model: str
    signature: str
    created_at: datetime #  hour, minute, second, microsecond and timezone info as datetime params

    def __init__(self, 
                 id: int,
                 responsible:User, 
                 location: str,
                 registration: str,
                 duration: int,
                 price: float,
                 paid: bool,
                 brand: str,
                 model: str,
                 signature: str,
                 created_at: datetime):
        self.id = id
        self.responsible = responsible
        self.location = location
        self.registration = registration
        self.duration = duration #minutes
        self.price = Decimal(price)
        self.paid = paid
        self.brand = brand
        self.model = model
        self.signature = signature
        self.created_at = created_at
    

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
            "signature": self.signature,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M")
        }
    
