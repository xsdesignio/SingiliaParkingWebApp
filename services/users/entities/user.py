from dataclasses import dataclass
import datetime
from enum import Enum

from services.zones.entities.zone import Zone

class UserRole(Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    EMPLOYEE = "EMPLOYEE"

    @classmethod
    def get_enum_value(cls, enum_member_name: str):
        for member in cls:
            if member.name == enum_member_name.upper():
                return member
        raise ValueError(f"No enum member with name '{enum_member_name}' found.")
    

@dataclass
class User:
    id: int
    role: UserRole
    name: str
    email: str
    password: str
    associated_zone: Zone = None
    created_at: datetime = datetime.datetime.now()

    def to_json(self):
        json_object = {
            'id': self.id,
            'role': self.role.name,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        if self.associated_zone != None:
            json_object['associated_zone'] = self.associated_zone.name

        return json_object