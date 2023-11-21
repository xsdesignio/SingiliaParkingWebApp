import datetime
from ..models.bulletin_model import BulletinModel
from ..models.available_bulletin_model import AvailableBulletinModel
from services.users.entities.user import User

from decimal import Decimal

from services.zones.entities.zone import Zone



def get_bulletins_attributes_count(start_date: datetime.datetime = None, end_date: datetime.datetime = None, zone: Zone = None, user: User = None):
    query_dict = {}

    available_bulletins: list[dict] = AvailableBulletinModel.get_available_bulletins()
        
    if start_date:
        query_dict["start_date"] = start_date

    if end_date:
        query_dict["end_date"] = end_date

    if(zone):
        query_dict["zone_id"] = zone.id
        
    if(user):
        query_dict["responsible_id"] = user.id


    # Obtaining the amount of bulletins that meet the conditions imposed by the query_dict dictionary and the value we want to count
    paid = BulletinModel.count_bulletins(**query_dict, paid = True) | 0;
    not_paid = BulletinModel.count_bulletins(**query_dict, paid = False) | 0;
        
    paid_by_card = BulletinModel.count_bulletins(**query_dict, payment_method = "CARD")
    paid_by_cash = BulletinModel.count_bulletins(**query_dict, payment_method = "CASH")

    bulletins_amount = {
        "bulletins_amount": paid + not_paid,
        "paid_amount": paid,
        "not_paid_amount": not_paid,
        "paid_by_cash": paid_by_cash,
        "paid_by_card": paid_by_card,
        "data_by_duration": [],
        "total_income": Decimal("0.00"),
    }

    for available_bulletin in available_bulletins:
        duration = available_bulletin["duration"]
        price = available_bulletin["price"]
        count_by_duration = BulletinModel.count_bulletins(**query_dict, duration = duration)
        
        paid = BulletinModel.count_bulletins(**query_dict, duration = duration, paid = True)
        not_paid = BulletinModel.count_bulletins(**query_dict, duration = duration, paid = False)

        paid_by_card = BulletinModel.count_bulletins(**query_dict, duration = duration, payment_method = "CARD")
        paid_by_cash = BulletinModel.count_bulletins(**query_dict, duration = duration, payment_method = "CASH")

        if count_by_duration == None:
            count_by_duration = 0
            
        data_by_duration_dict = {
            "duration": duration,
            "amount": count_by_duration,
            "paid_amount": paid_by_card,
            "not_paid_amount": paid_by_cash,
            "paid_by_card": paid_by_card,
            "paid_by_cash": paid_by_cash,
            "total_income": count_by_duration * price,
        }

        bulletins_amount["data_by_duration"].append(data_by_duration_dict)

        bulletins_amount["total_income"] += data_by_duration_dict["total_income"]


    return bulletins_amount
    
