from pydantic import BaseModel

class Crop(BaseModel):
    name: str
    temp_min: float
    temp_max: float

class CropInfo(Crop):
    crop_id: str    
    pass

class CropCreate(Crop):
    pass

class CropRisk(Crop):
    temperature: float
    risk_status: int
    risk_desc: str
    pass
