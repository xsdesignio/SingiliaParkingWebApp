from dataclasses import dataclass
from time import time




@dataclass
class OpenSpan:
    """
        Does not contain an id because is represented
        in the database as a type
    """
    openTime: time 
    closeTime: time 

    def to_dict(self):
        return {
            "openTime": self.openTime.strftime('%H:%M') if self.openTime else None,
            "closeTime": self.closeTime.strftime('%H:%M') if self.closeTime else None
        }

@dataclass
class DailySchedule:
    id: int
    openSpans: list[OpenSpan]


    def to_dict(self):
        return {
            "openSpans": [openSpan.to_dict() for openSpan in self.openSpans]
        }


@dataclass 
class ScheduleWeek:
    # id is not needed as there is just one ScheduleWeek object shared along the app
    monday: DailySchedule
    tuesday: DailySchedule
    wednesday: DailySchedule
    thursday: DailySchedule
    friday: DailySchedule
    saturday: DailySchedule
    sunday: DailySchedule

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
