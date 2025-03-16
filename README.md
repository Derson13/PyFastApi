# Helios Tech Interview API

# Helios Tech Interview API

## Prerequisites: Service Account JSON Key
Before running the project, you need to download the **Google Cloud Service Account JSON key** file. This file should be placed in two locations:

1. In the **root directory** of the project.
2. In the **`bq_start`** folder.

The file should be named `service-api.json`.
---

This FastAPI application provides an API to query crop information from BigQuery in the Helios Tech Interview Project.
[Helios Tech Interview API](https://helios-api-200118253515.us-east1.run.app/docs)

## Documentation
#### Documentation of the solution implemented in big query and api implemented in cloud run available in the index.html file
```bash
./docs/index.html
```
## Prerequisites
- Python 3.11+
- Docker
- GCP Service Account with BigQuery access

## Install dependencies:
```bash
pip install -r requirements.txt
```

## Start Project in Big Query
```bash
python .\bq_start\bq_init.py
```

## Running Locally
```bash
uvicorn main:app --reload
```
## Implement in Google:
1. Auth Google:
```bash
gcloud auth activate-service-account --key-file=".\service-api.json"
gcloud auth list
gcloud auth configure-docker
```

2. Deploy to Cloud Run:
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