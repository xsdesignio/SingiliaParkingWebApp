import datetime
from ..models.bulletin_model import BulletinModel

from decimal import Decimal

from services.zones.entities.zone import Zone



def get_bulletins_attributes_count(start_date: datetime.datetime = None, end_date: datetime.datetime = None, zone: Zone = None):
        query_dict = {}
    
        if start_date:
            query_dict["start_date"] = start_date

        if end_date:
            query_dict["end_date"] = end_date

        if(zone):
            query_dict["zone_id"] = zone.id


        paid = BulletinModel.count_bulletins(**query_dict, paid = False)
        not_paid = BulletinModel.count_bulletins(**query_dict, paid = True)
        duration_of_30 = BulletinModel.count_bulletins(**query_dict, duration = 30)
        duration_of_60 = BulletinModel.count_bulletins(**query_dict, duration = 60)
        duration_of_90 = BulletinModel.count_bulletins(**query_dict, duration = 90)
        duration_of_120 = BulletinModel.count_bulletins(**query_dict, duration = 120)

        if paid is None:
            paid = 0
        if not_paid is None:
            not_paid = 0
        

        bulletins_amount = {
            "bulletins_amount": paid + not_paid,
            "paid": paid,
            "not_paid": not_paid,
            "duration_of_30": duration_of_30,
            "total_income_by_30": round(duration_of_30 * get_prices_by_duration(30), 2),
            "duration_of_60": duration_of_60,
            "total_income_by_60": round(duration_of_60 * get_prices_by_duration(60), 2),
            "duration_of_90": duration_of_90,
            "total_income_by_90": round(duration_of_90 * get_prices_by_duration(90), 2),
            "duration_of_120": duration_of_120,
            "total_income_by_120": round(duration_of_120 * get_prices_by_duration(120), 2),
        }

        total_income = round(bulletins_amount["total_income_by_30"] + bulletins_amount["total_income_by_60"] + bulletins_amount["total_income_by_90"] + bulletins_amount["total_income_by_120"]
                               , 2)
        bulletins_amount["total_income"] = total_income


        return bulletins_amount
    



def get_prices_by_duration(duration):
    """Return a dictionary with the prices by duration"""
    
    if duration <= 30:
        return 0.7
    elif duration <= 60:
        return 0.9
    elif duration <= 90:
        return 1.4
    elif duration <= 120:
        return 1.8
    elif duration <= 180:
        return 3.6
    elif duration <= 240:
        return 4.5