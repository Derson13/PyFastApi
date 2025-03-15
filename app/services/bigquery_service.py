from google.cloud import bigquery
from fastapi import HTTPException
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize BigQuery client
client = bigquery.Client(project="helios-tech-interview-project")

def results_to_dict(results):
    df = pd.DataFrame([dict(row) for row in results])
    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="Empty return!"
        )
    return df.to_dict(orient='records')

def execute_query(query: str):
    """
    Execute a BigQuery query and return the results as a dictionary
    """
    try:
        query_job = client.query(query)
        results = query_job.result()        
        return results_to_dict(results)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while querying BigQuery: {str(e)}"
        ) 