from fastapi import APIRouter, HTTPException
from typing import Optional, List
import app.models.growing as model
import app.services.bigquery_service as bq

router = APIRouter()

@router.get("/growing-info/", response_model=List[model.GrowingInfo])
async def get_growing_info(h3index_num: Optional[int] = None, crop_id: Optional[str] = None):
    """    
    Get growing seasons information by passing h3index_num or crop_id. 
    - At least one parameter must be provided.
    """
    if not h3index_num and not crop_id:
        raise HTTPException(
            status_code=400,
            detail="Either h3index_num or crop_id must be provided"
        )

    query = "SELECT * FROM `helios-tech-interview-project.result_test.tb_1_growing_seasons` WHERE 1=1"

    if h3index_num:
        query += f" AND h3index_num = {h3index_num}"        
    if crop_id:
        query += f" AND crop_id = '{crop_id}'"        

    return bq.exec_query_bq(query)