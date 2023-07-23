from enum import Enum


class PaymentMethod(Enum):
    CARD = "CARD"
    CASH = "CASH"

    @classmethod
    def get_enum_value(cls, enum_member_name: str):
        for member in cls:
            if member.name == enum_member_name.upper():
                return member
        raise ValueError(f"No enum member with name '{enum_member_name}' found.")