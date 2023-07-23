from dataclasses import dataclass
from services.users.entities.user import User


@dataclass
class Zone:
    id: int
    name: str
    responsibles: list[User] = None
