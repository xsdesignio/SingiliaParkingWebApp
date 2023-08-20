from enum import Enum


class PaymentMethod(Enum):
    CARD = "CARD"
    CASH = "CASH"

    @classmethod
    def get_enum_value(cls, enum_member_name: str):

        if(enum_member_name == None):
            return None
        
        for member in cls:
            if member.name == enum_member_name.upper():
                return member
        
        # If the enum_member_name doesn't exists return None
        return None