from decimal import Decimal


class AvailableTicket:
    id: int
    duration: str
    duration_minutes: int
    price: Decimal


    def __init__(self, id, duration, duration_minutes, price):
        self.id = id
        self.duration = duration.upper()
        self.duration_minutes = duration_minutes
        self.price = price

    def to_json(self):
        return {
            'id': self.id,
            'duration': self.duration,
            'duration_minutes': self.duration_minutes,
            'price': self.price
        }

    @staticmethod
    def from_dict(ticket_dict):
        return AvailableTicket(
            id=ticket_dict['id'],
            duration=ticket_dict['duration'],
            duration_minutes=ticket_dict['duration_minutes'],
            price=ticket_dict['price'],
        )