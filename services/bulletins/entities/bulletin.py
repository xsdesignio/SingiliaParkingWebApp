from dataclasses import dataclass

from datetime import datetime
from decimal import Decimal
from services.users.entities.user import User
from services.zones.entities.zone import Zone
from services.utils.payment_methods import PaymentMethod



@dataclass
class Bulletin:
    # Creation Properties
    id: str
    responsible: User
    zone: Zone
    registration: str
    precept: str 

    # Anulation Properties
    duration: int = None
    price: Decimal = None
    payment_method: PaymentMethod = None
    paid: bool = True
    created_at: datetime = datetime.now() 

    # Optional
    brand: str = None
    model: str = None
    color: str = None

    """ 
    def __post_init__(self):
        if not isinstance(self.price, Decimal):
            self.price = Decimal(self.price)
    """

    def to_json(self):
        json_obj =  {
            "id": self.id,
            "responsible": self.responsible.name if self.responsible else "Usuario eliminado",
            "zone": self.zone.name if self.zone else "Zona eliminada",
            "registration": self.registration,
            "precept": self.precept,
            "paid": self.paid,
            "brand": self.brand,
            "model": self.model,
            "color": self.color,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M")
        }
        if self.price:
            json_obj["price"] = self.price

        if self.duration:
            json_obj["duration"] = self.duration

        if self.payment_method:
            json_obj["payment_method"] = self.payment_method.value
        else:
            json_obj["payment_method"] = "El boletín aún no ha sido pagado"

        return json_obj
    
