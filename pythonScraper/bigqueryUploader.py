import os
import json
import pandas as pd
from google.cloud import bigquery

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

client = bigquery.Client()

#BigQUery table info
PROJECT_ID = "pythonscraper-453902"
DATASET_ID = "articles_data"
TABLE_ID = "articles"
TABLE_PATH = f"{DATASET_ID}.{TABLE_ID}"

# Uploads Json data to BigQuery table
def upload_to_bigquery(df):
    """
    Accepts a JSON object (list of articles) and uploads it to BigQuery.
    """
    #Table schema
    schema = [
        bigquery.SchemaField("Title", "STRING"),
        bigquery.SchemaField("Kicker", "STRING"),
        bigquery.SchemaField("Image", "STRING"),
        bigquery.SchemaField("URL", "STRING"),
        bigquery.SchemaField("Word_Count", "INTEGER"),
        bigquery.SchemaField("Character_Count", "INTEGER"),
        bigquery.SchemaField("Capitalized_Words", "STRING", mode="REPEATED")
    ]

    #BigQuery upload job
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND
    )

    #Upload DF to table
    try:
        print(f"Uploading {len(df)} articles to BigQuery table: {TABLE_PATH}")
        job = client.load_table_from_dataframe(df, TABLE_PATH, job_config=job_config)
        job.result()
        print(f"Data uploaded successfully to the table: {TABLE_PATH}")
        return True
    except Exception as e:
        print(f"Error uploading data to BigQuery: {e}")
        return False
