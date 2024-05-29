from dataclasses import dataclass
from time import time


@dataclass
class ScheduleDay:
    id: int
    openTime: time 
    closeTime: time 

    def to_dict(self):
        return {
            "openTime": self.openTime.strftime('%H:%M') if self.openTime else None,
            "closeTime": self.closeTime.strftime('%H:%M') if self.closeTime else None
        }


@dataclass 
class ScheduleWeek:
    # id is not needed as there is just one ScheduleWeek object shared along the app
    monday: ScheduleDay
    tuesday: ScheduleDay
    wednesday: ScheduleDay
    thursday: ScheduleDay
    friday: ScheduleDay
    saturday: ScheduleDay
    sunday: ScheduleDay

    def to_dict(self):
        return {
            'monday': self.monday.to_dict() if self.monday else None,
            'tuesday': self.tuesday.to_dict() if self.tuesday else None,
            'wednesday': self.wednesday.to_dict() if self.wednesday else None,
            'thursday': self.thursday.to_dict() if self.thursday else None,
            'friday': self.friday.to_dict() if self.friday else None,
            'saturday': self.saturday.to_dict() if self.saturday else None,
            'sunday': self.sunday.to_dict() if self.sunday else None
        }
