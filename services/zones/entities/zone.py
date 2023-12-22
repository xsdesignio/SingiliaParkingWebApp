from dataclasses import dataclass


@dataclass
class Zone:
    id: int
    name: str
    identifier: str
    tickets: int
    bulletins: int

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "identifier": self.identifier,
            "tickets": self.tickets,
            "bulletins": self.bulletins
        }
