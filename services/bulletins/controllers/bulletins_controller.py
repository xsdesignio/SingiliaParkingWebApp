import datetime
from ..models.bulletin_model import BulletinModel

from services.zones.entities.zone import Zone



def get_bulletins_attributes_count(start_date: datetime.datetime = None, end_date: datetime.datetime = None, zone: Zone = None):
        query_dict = {}
    
        if start_date:
            query_dict["start_date"] = start_date

        if end_date:
            query_dict["end_date"] = end_date

        if(zone):
            query_dict["zone_id"] = zone.id


        paid_by_card = BulletinModel.count_bulletins(**query_dict, payment_method = "CARD")
        paid_by_cash = BulletinModel.count_bulletins(**query_dict, payment_method = "CASH")
        duration_of_30 = BulletinModel.count_bulletins(**query_dict, duration = 30)
        duration_of_60 = BulletinModel.count_bulletins(**query_dict, duration = 60)
        duration_of_90 = BulletinModel.count_bulletins(**query_dict, duration = 90)
        duration_of_120 = BulletinModel.count_bulletins(**query_dict, duration = 120)

        if paid_by_card is None:
            paid_by_card = 0
        if paid_by_cash is None:
            paid_by_cash = 0
        

        bulletins_amount_by_data = {
            "total_tickets": paid_by_card + paid_by_cash,
            "paid_by_card": paid_by_card,
            "paid_by_cash": paid_by_cash,
            "duration_of_30": duration_of_30,
            "duration_of_60": duration_of_60,
            "duration_of_90": duration_of_90,
            "duration_of_120": duration_of_120,
        }


        return bulletins_amount_by_data
    
