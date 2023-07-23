import datetime
from services.bulletins.models.bulletin_model import BulletinModel

from services.zones.entities.zone import Zone

def get_bulletins_attributes_count(start_date: datetime.datetime = None, end_date: datetime.datetime = None, zone: Zone = None):
        """Return a dictionary with the variables and their count"""

        paid_by_card = BulletinModel.count_bulletins_by_attribute('paid', True, start_date, end_date, zone)
        paid_by_cash = BulletinModel.count_bulletins_by_attribute('paid', False, start_date, end_date, zone)
        duration_of_30 = BulletinModel.count_bulletins_by_attribute('duration', 30, start_date, end_date, zone)
        duration_of_60 = BulletinModel.count_bulletins_by_attribute('duration', 60, start_date, end_date, zone)
        duration_of_90 = BulletinModel.count_bulletins_by_attribute('duration', 90, start_date, end_date, zone)
        duration_of_120 = BulletinModel.count_bulletins_by_attribute('duration', 120, start_date, end_date, zone)

        tickets_amount_by_data = {
            "paid_by_card": paid_by_card,
            "paid_by_cash": paid_by_cash,
            "duration_of_30": duration_of_30,
            "duration_of_60": duration_of_60,
            "duration_of_90": duration_of_90,
            "duration_of_120": duration_of_120,
        }

        return tickets_amount_by_data
    
