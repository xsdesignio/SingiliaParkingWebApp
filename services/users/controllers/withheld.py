from ..entities.user import User
from ..models.user_model import UserModel
from decimal import Decimal


def add_withheld_to_user(user: User, amount: float):
    #print the type of the amount and the type of the user.withheld
    print("This do is executed")
    updated_withheld = user.withheld + Decimal(amount);
    updated_user = UserModel.update_user(user.id, {
        "withheld": updated_withheld
        }
    )
    print("Updated user: ", updated_user)
    return updated_user

def substract_withheld_to_user(user: User, amount: float):
    updated_withheld = user.withheld - Decimal(amount)
    updated_user = UserModel.update_user(user.id, {
        "withheld": updated_withheld
        }
    )
    return updated_user

def pay_withheld_to_user(user: User):
    updated_user = UserModel.update_user(user.id, {
        "withheld": 0
        }
    )

    return updated_user