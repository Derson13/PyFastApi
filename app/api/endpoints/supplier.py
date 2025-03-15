from fastapi import APIRouter, HTTPException
from typing import Optional, List
from app.models.supplier import SupplierInfo
import app.services.bigquery_service as bq

router = APIRouter()

@router.get("/supplier/", response_model=List[SupplierInfo])
async def get_supplier_info(poi_id: Optional[str] = None, supplier_name: Optional[str] = None):
    """    
    Get supplier information by passing supplier id or supplier name. 
    At least one parameter must be provided.
    """
    if not poi_id and not supplier_name:
        raise HTTPException(
            status_code=400,
            detail="Either poi_id or supplier_name must be provided"
        )

    query = "SELECT * FROM `helios-tech-interview-project.shared.places_of_interest`"      
    
    if poi_id:
        query += f" WHERE poi_id = '{poi_id}'"
    if supplier_name:
        query += f" WHERE supplier_name = '{supplier_name}'"

    return bq.exec_query_bq(query) 