from dataclasses import dataclass
import datetime
from enum import Enum

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
    created_at: datetime = datetime.datetime.now()

    def to_json(self):
        return {
            'id': self.id,
            'role': self.role.name,
            'name': self.name,
            'email': self.email,
            'created_at': str(self.created_at)
        }