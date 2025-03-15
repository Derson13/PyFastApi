from fastapi import APIRouter, HTTPException
from typing import Optional, List
import app.models.crop as model
import app.services.bigquery_service as bq

router = APIRouter()

@router.get("/crop-info/", response_model=List[model.CropInfo])
async def get_crop_info(crop_id: Optional[str] = None, name: Optional[str] = None):
    """    
    Get crop information by passing crop id or name. 
    - At least one parameter must be provided.
    """
    if not crop_id and not name:
        raise HTTPException(
            status_code=400,
            detail="Either crop_id or name must be provided"
        )

    query = "SELECT * FROM `helios-tech-interview-project.shared.crop_info`"
    
    if crop_id:
        query += f" WHERE crop_id = '{crop_id}'"        
    if name:
        query += f" WHERE name = '{name}'"        

    return bq.exec_query_bq(query)

@router.post("/crop-insert/", response_model=dict)
async def create_crop(crop: model.CropCreate):
    """
    Create a new crop
    """
    # Check if crop_id already exists
    query = f"""SELECT COUNT(*) as count 
               FROM `helios-tech-interview-project.shared.crop_info` 
               WHERE name = '{crop.name}'"""
    
    result = bq.exec_query_bq(query)
    if result[0]["count"] > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Crop with name {crop.name} already exists"
        )
    
    query = f"""INSERT INTO `helios-tech-interview-project.shared.crop_info` 
                      (crop_id, name, temp_min, temp_max) 
                      VALUES (
                           GENERATE_UUID()
                          ,'{crop.name}'
                          ,{crop.temp_min}
                          ,{crop.temp_max}
                      )"""

    return bq.exec_dml_query_bq(query)

@router.get("/crop-risk-temp/", response_model=List[model.CropRisk])
async def get_crop_risk(temperature: float, crop_id: Optional[str] = None, name: Optional[str] = None):
    """    
    Get information about the crop risk by entering the temperature and either crop_id or name.
    
    Parameters:
    - temperature: Current temperature to check risk
    - crop_id: Optional crop ID
    - name: Optional crop name
    At least crop_id or name must be provided.
    """
    if not crop_id and not name:
        raise HTTPException(
            status_code=400,
            detail="Either crop_id or name must be provided"
        )

    search_value = crop_id if crop_id else name
    query = f"CALL `helios-tech-interview-project.result_test.pr_3_api_crop_risk`('{search_value}', {temperature});"
    
    return bq.exec_query_bq(query)