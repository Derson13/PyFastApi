from fastapi import FastAPI, HTTPException
from google.cloud import bigquery
from typing import Optional
from pydantic import BaseModel
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Helios API")

# Initialize BigQuery client
client = bigquery.Client(project="helios-tech-interview-project")

class CropInfo(BaseModel):
    crop_id: str
    name: str    
    temp_min: float
    temp_max: float    

class SupplierInfo(BaseModel):
    poi_id: str
    supplier_name: str  
    country_code: str
    country_name: str
    h3index_num: int
    crop_id:str

def get_bq(query):
    try:
        query_job = client.query(query)
        results = query_job.result()        
        data = results_to_dict(results)
            
        return data
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while querying BigQuery: {str(e)}"
        )

def results_to_dict(results):
    df = pd.DataFrame([dict(row) for row in results])
    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="Empty return!"
        )

    return df.to_dict(orient='records')

@app.get("/crop-info/", response_model=list[CropInfo])
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
    
    if crop_id:query += f" WHERE crop_id = '{crop_id}'"
    if name:query += f" WHERE name = '{name}'"

    data = get_bq(query)

    return data

@app.get("/supplier/", response_model=list[SupplierInfo])
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
    
    if poi_id:query += f" WHERE poi_id = '{poi_id}'"
    if supplier_name:query += f" WHERE supplier_name = '{supplier_name}'"

    data = get_bq(query)
    
    return data