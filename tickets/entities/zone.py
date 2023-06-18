from datetime import datetime

class Zone:
    id: int
    name:str
    created_at: datetime

    def __init__(self, id:int, name:str, created_at:datetime):
        self.id = id
        self.name = name
        self.created_at = created_at