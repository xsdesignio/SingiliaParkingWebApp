from flask import session

from services.users.models.user_model import UserModel
from services.users.entities.user import User


def signup_user(role:str, name: str, email: str, password: str) -> User:
    """
        Returns True if user is added successfully
        Returns False if user data isn't correct
    """
     
    # checking introduced params
    role = role.upper() # Roles are managed in upper case
    data_is_correct: bool = check_data(role, name, email, password)
    # If data isn't correct return None
    if not data_is_correct:
        return None
    
    # Store user and check if is stored correctly
    user_stored: User = UserModel.create_user(role, name, email, password)

    if user_stored == None:
        return None
    
    # Adding user to server session
    session['id'] = user_stored.id
    session['role'] = role
    session['name'] = name
    session['email'] = email
    
    return user_stored




def check_data(role:str, name: str, email: str, password: str) -> bool:
    """
        Returns true if the params introduced follow the defined rules
    """
    role = role.upper()
    if not (role == "ADMIN" or role == "MANAGER" or role == "EMPLOYE"):
        return False
    
    
    if name == "" or name == None:
        return False
    
    # Checking email is not none and that letters are more than 4
    if  email == None or len(email) < 5:
        return False
    if '@' not in email or '.' not in email:
        return False
    
    if len(password) < 8:
        return False
    
    return True