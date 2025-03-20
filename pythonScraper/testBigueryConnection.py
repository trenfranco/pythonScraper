from google.cloud import bigquery
import os

# Set authentication key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

# Initialize BigQuery Client
client = bigquery.Client()

# Print available datasets
datasets = list(client.list_datasets())
for dataset in datasets:
    print(f"Dataset: {dataset.dataset_id}")

print("Connection successful")
