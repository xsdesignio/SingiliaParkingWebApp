from typing import Optional
from datetime import datetime, timedelta
from services.zones.models.zone_model import ZoneModel


def parse_date(date_str: Optional[str], default: datetime) -> datetime:
    """Parse date string into datetime or return default if not provided."""
    if date_str:
        return datetime.strptime(date_str, '%Y-%m-%d')
    return default



def get_queries_from_request_data(data):
    start_date = parse_date(data.get('start_date'), datetime.now() - timedelta(days=30))
    end_date = parse_date(data.get('end_date'), datetime.now())
    zone_name = data.get('zone')

    query_values = {
        "start_date": start_date, 
        "end_date":  end_date, 
    }
    
    if zone_name != 'all' and zone_name != None:
        zone = ZoneModel.get_zone_by_name(zone_name)
        query_values["zone_id"] = zone.id

    if data.get('responsible_id'):
        query_values["responsible_id"] = data.get('responsible_id')

    if data.get('zone_id'):
        query_values["zone_id"] = data.get('zone_id')

    return query_values



def get_range_from_page(page):
    page_amount = 50
    default_range = (0, page_amount)
    
    if page == None:
        return default_range
    return (page*page_amount, (page+1)*page_amount)
    