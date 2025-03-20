import functions_framework
import requests
import google.auth
from google.auth.transport.requests import Request

PROJECT_ID = "pythonscraper-453902"
REGION = "us-central1"
JOB_NAME = "scrapejob"

@functions_framework.http
def trigger_scraper_job(request):
    """Executes the cloud run job"""
    
    url = f"https://us-central1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/{PROJECT_ID}/jobs/{JOB_NAME}:run"
    
    #Auth token
    credentials, _ = google.auth.default()
    credentials.refresh(Request())
    headers = {
        "Authorization": f"Bearer {credentials.token}",
        "Content-Type": "application/json"
    }
    
    #Request to execute job
    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        return "Scraper executed succesfully", 200
    else:
        return f"Error executing: {response.text}", 500
