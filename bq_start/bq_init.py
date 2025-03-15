from google.cloud import bigquery
from google.oauth2 import service_account
from pathlib import Path
import os

def init_bigquery_objects():
    """
    Initialize BigQuery objects by executing all SQL files in the directory
    """
    try:
        # Setup credentials
        service_account_path = 'service-api.json'
        credentials = service_account.Credentials.from_service_account_file(service_account_path)
        client = bigquery.Client(credentials=credentials, project=credentials.project_id)
        
        # Get current directory where the SQL files are
        current_dir = Path(__file__).parent
        
        # Get all .sql files in the current directory
        sql_files = list(current_dir.glob("*.sql"))
        
        if not sql_files:
            print("No SQL files found in the directory")
            return
        
        # Execute each SQL file
        for sql_file in sql_files:
            try:
                print(f"\nExecuting {sql_file.name}...")
                
                # Read SQL content
                with open(sql_file, 'r', encoding='utf-8') as f:
                    sql_content = f.read()
                
                    query_job = client.query(sql_content)
                    query_job.result()  # Wait for query to complete
                    
                print(f"Successfully executed {sql_file.name}")
                
            except Exception as e:
                print(f"Error executing {sql_file.name}: {str(e)}")
                
        print("\nFinished executing all SQL files")
        
    except Exception as e:
        print(f"Error initializing BigQuery objects: {str(e)}")

if __name__ == "__main__":
    init_bigquery_objects()