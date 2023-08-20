from dataclasses import dataclass

from datetime import datetime
from decimal import Decimal
from services.users.entities.user import User
from services.zones.entities.zone import Zone
from services.utils.payment_methods import PaymentMethod



@dataclass
class Bulletin:
    id: int
    responsible: User
    zone: Zone
    duration: int # in minutes
    registration: str
    price: Decimal
    payment_method: PaymentMethod = None
    paid: bool = True
    created_at: datetime = datetime.now() 

    # Optional
    brand: str = None
    model: str = None
    color: str = None



    def __post_init__(self):
        if not isinstance(self.price, Decimal):
            self.price = Decimal(self.price)


    def to_json(self):
        json_obj =  {
            "id": self.id,
            "responsible": self.responsible.name,
            "zone": self.zone.name,
            "duration": self.duration, 
            "registration": self.registration,
            "price": self.price,
            "paid": self.paid,
            "brand": self.brand,
            "model": self.model,
            "color": self.color,

            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M")
        }
        if self.payment_method:
            json_obj["payment_method"] = self.payment_method.value
        else:
            json_obj["payment_method"] = "El boletín aún no ha sido pagado"

        return json_obj
    
