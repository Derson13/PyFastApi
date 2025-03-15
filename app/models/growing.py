from datetime import date
from pydantic import BaseModel

class Growing(BaseModel):
    h3index_num: int
    crop_id: str
    season_start_week: int
    season_end_week: int
    season_start_date: date
    season_end_date: date
    length_of_season_weeks: int
    length_of_season_days: int

class GrowingInfo(Growing):
    pass