from fastapi import FastAPI, HTTPException
from google.cloud import bigquery
from typing import Optional
from pydantic import BaseModel
import pandas as pd

app = FastAPI(title="Helios Tech Interview API")

# Initialize BigQuery client
client = bigquery.Client(project="helios-tech-interview-project")

class CropInfo(BaseModel):
    crop_id: str
    name: str    

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
    
    if crop_id:query += f" WHERE crop_id = {crop_id}"
    if name:query += f" WHERE name = {name}"

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

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"} 