from pydantic import BaseModel

class Supplier(BaseModel):
    supplier_name: str  
    country_code: str
    country_name: str
    h3index_num: int
    crop_id: str 

class SupplierInfo(Supplier):
    poi_id: str
    pass