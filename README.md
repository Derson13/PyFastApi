# Helios Tech Interview API

This FastAPI application provides an API to query crop information from BigQuery in the Helios Tech Interview Project.

## Prerequisites

- Python 3.11+
- Docker (optional)
- GCP Service Account with BigQuery access

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running Locally
```bash
uvicorn main:app --reload
```

## Running with Docker

1. Build the image:
```bash
docker build -t gcr.io/helios-tech-interview-project/helios-api .
```

2. Run the container:
```bash
docker run -p 8080:8080 -v /path/to/service-account:/app/service-account.json -e GOOGLE_APPLICATION_CREDENTIALS=/app/service-account.json helios-api
```

3. Auth Google:
```bash
gcloud auth activate-service-account --key-file=".\service-api.json"
gcloud auth list
gcloud auth configure-docker
```

4. Deploy to Cloud Run:
```bash
docker build -t gcr.io/helios-tech-interview-project/helios-api .
docker push gcr.io/helios-tech-interview-project/helios-api

gcloud run deploy helios-api 
  --image gcr.io/helios-tech-interview-project/helios-api 
  --platform managed 
  --region us-east1 
  --allow-unauthenticated 
  --service-account=200118253515-compute@developer.gserviceaccount.com 
  --set-env-vars="GOOGLE_CLOUD_PROJECT=helios-tech-interview-project"
```