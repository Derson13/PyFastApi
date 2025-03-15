from google.cloud import bigquery
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

def init_bigquery_objects():
    """
    Initialize BigQuery objects by executing all SQL files in the sql_scripts directory
    """
    try:
        # Initialize BigQuery client
        client = bigquery.Client(project="helios-tech-interview-project")
        
        # Get the directory where this script is located
        current_dir = Path(__file__).parent
        sql_dir = current_dir / "sql_scripts"
        
        # Check if directory exists
        if not sql_dir.exists():
            print(f"Creating SQL scripts directory at {sql_dir}")
            sql_dir.mkdir(exist_ok=True)
            return
        
        # Get all .sql files
        sql_files = list(sql_dir.glob("*.sql"))
        
        if not sql_files:
            print("No SQL files found in the directory")
            return
        
        print(f"Found {len(sql_files)} SQL files to execute")
        
        # Execute each SQL file
        for sql_file in sql_files:
            try:
                print(f"\nExecuting {sql_file.name}...")
                
                # Read SQL content
                with open(sql_file, 'r', encoding='utf-8') as f:
                    sql_content = f.read()
                
                # Split the content by semicolon to handle multiple statements
                statements = sql_content.split(';')
                
                # Execute each statement
                for statement in statements:
                    if statement.strip():  # Skip empty statements
                        query_job = client.query(statement)
                        query_job.result()  # Wait for query to complete
                        
                print(f"Successfully executed {sql_file.name}")
                
            except Exception as e:
                print(f"Error executing {sql_file.name}: {str(e)}")
                
        print("\nFinished executing all SQL files")
        
    except Exception as e:
        print(f"Error initializing BigQuery objects: {str(e)}")

if __name__ == "__main__":
    init_bigquery_objects() 