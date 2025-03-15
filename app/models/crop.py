from pydantic import BaseModel

class CropInfo(BaseModel):
    crop_id: str
    name: str    
    temp_min: float
    temp_max: float 