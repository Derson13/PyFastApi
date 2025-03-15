from fastapi import APIRouter, HTTPException
from typing import Optional, List
from app.models.crop import CropInfo
from app.services.bigquery_service import execute_query

router = APIRouter()

@router.get("/crop-info/", response_model=List[CropInfo])
async def get_crop_info(crop_id: Optional[str] = None, name: Optional[str] = None):
    """    
    Get crop information by passing crop id or name. 
    At least one parameter must be provided.
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

    return execute_query(query) 