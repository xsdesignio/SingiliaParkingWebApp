from decimal import Decimal


class AvailableBulletin:
    id: int
    duration: str
    price: Decimal


    def __init__(self, id, duration, price):
        self.id = id
        self.duration = duration
        self.price = price

    def to_json(self):
        return {
            'id': self.id,
            'duration': self.duration,
            'price': self.price
        }

    @staticmethod
    def from_dict(ticket_dict):
        return AvailableBulletin(
            id=ticket_dict['id'],
            duration=ticket_dict['duration'],
            price=ticket_dict['price'],
        )