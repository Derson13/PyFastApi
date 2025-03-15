from pydantic import BaseModel

class SupplierInfo(BaseModel):
    poi_id: str
    supplier_name: str  
    country_code: str
    country_name: str
    h3index_num: int
    crop_id: str 