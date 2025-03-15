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

def exec_query_bq(query: str):
    """
    Execute a BigQuery query and return the results as a dictionary
    """
    try:
        print(query)
        query_job = client.query(query)
        results = query_job.result()        
        return results_to_dict(results)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while querying BigQuery: {str(e)}"
        )

def exec_dml_query_bq(query: str):
    """
    Execute a DML query (INSERT, UPDATE, DELETE) and return success status
    """
    try:
        print(query)
        query_job = client.query(query)
        query_job.result()
        
        # Get number of affected rows
        num_affected = query_job.num_dml_affected_rows        
        return {
            "success": True,
            "affected_rows": num_affected,
            "message": f"Operation completed successfully. Rows affected: {num_affected}"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while executing DML operation: {str(e)}"
        ) 