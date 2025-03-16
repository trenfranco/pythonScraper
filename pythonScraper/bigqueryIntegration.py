import os
import json
import pandas as pd
from google.cloud import bigquery
from google.cloud import secretmanager

#Project info
PROJECT_ID = "pythonscraper-453902"
DATASET_ID = "pythonscraper-453902.articles_data"
TABLE_ID = "pythonscraper-453902.articles_data.articles"
TABLE_PATH = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

#Retrieve bigquery credentials
def get_bigquery_credentials():
    """Retrieve the Service Account Key from Google Secrets Manager."""
    client = secretmanager.SecretManagerServiceClient()
    secret_name = f"projects/{PROJECT_ID}/secrets/bigquery-key/versions/latest"
    response = client.access_secret_version(name=secret_name)
    return json.loads(response.payload.data.decode("UTF-8"))

#Load credentials
credentials_dict = get_bigquery_credentials()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

# Save credentials to a temporary JSON file
with open(os.environ["GOOGLE_APPLICATION_CREDENTIALS"], "w") as key_file:
    json.dump(credentials_dict, key_file)

#Init client
client = bigquery.Client()

#Load articles from json
input_file = "scrapedArticles.json"
df = pd.read_json(input_file)

schema = [
    bigquery.SchemaField("Title", "STRING"),
    bigquery.SchemaField("Kicker", "STRING"),
    bigquery.SchemaField("Image", "STRING"),
    bigquery.SchemaField("URL", "STRING"),
    bigquery.SchemaField("Word_Count", "INTEGER"),
    bigquery.SchemaField("Character_Count", "INTEGER"),
    bigquery.SchemaField("Capitalized_Words", "STRING", mode="REPEATED")
]

#Upload job
job_config = bigquery.LoadJobConfig(
    schema=schema,
    write_disposition=bigquery.WriteDisposition.WRITE_APPEND
)

#Insert data into BigQuery table
job = client.load_table_from_dataframe(df, TABLE_PATH, job_config=job_config)
job.result()  # Wait for the job to complete

print(f"Data uploaded successfully: {TABLE_PATH}")
