from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from services.users.entities.user import User
from services.zones.entities.zone import Zone
from services.utils.payment_methods import PaymentMethod

@dataclass
class Ticket:
    id: str
    responsible: User
    zone: Zone
    duration: int # in minutes
    registration: str
    price: Decimal
    payment_method: PaymentMethod = PaymentMethod.CASH
    paid: bool = True
    created_at: datetime = datetime.now() 

    def __post_init__(self):
        """This code is executed after the object is created and ensures that the price is a Decimal object."""
        if not isinstance(self.price, Decimal):
            self.price = Decimal(self.price)
    

    def to_json(self):
        return {
            'id': self.id,
            'responsible': self.responsible.name if self.responsible else 'Usuario eliminado',
            'zone': self.zone.name if self.zone else 'Zona eliminada',
            'duration': self.duration,
            'registration': self.registration,
            'price': self.price,
            'payment_method': self.payment_method.value,
            'paid': self.paid,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M")
        }
    
