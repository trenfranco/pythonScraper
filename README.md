# Web Scraper with BigQuery Integration

This project is a web scraper built with **Python** and **Selenium** that extracts news articles from https://www.yogonet.com/international/. The extracted data is processed using Pandas and uploaded to Google BigQuery for further analysis.

# How tu externally run and view the extracted data using http request:
**To run**, go to this url that executes the google scrape job: https://us-central1-pythonscraper-453902.cloudfunctions.net/trigger_scraper_job

Wait a couple of minutes to finish the execution and navigate here to **view the extracted data**: https://console.cloud.google.com/bigquery?ws=!1m5!1m4!4m3!1spythonscraper-453902!2sarticles_data!3sarticles

Another option to get the google job URL is to run the main.py
------------------------------------------------------
#scrape.py
1. Uses **Selenium** with XPATH to extract news articles.
2. Extracts relevant details like **title, kicker, URL, image, and text metrics**.
3. Saves the data into a **Pandas DataFrame**.
4. Uploads the structured data to **Google BigQuery** for further analysis.

The script is designed to run **inside a Docker container** or be deployed on **Google Cloud Run**.
------------------------------------------------------
#bigqueryUploader.py

1. **Authenticates with Google Cloud** using a service account.
2. **Defines a structured schema** for storing articles.
3. **Uploads data** extracted by the scraper to BigQuery.
4. **Handles errors gracefully** and returns success or failure.

#main.py
This script allows external users to **start the scraper remotely** using an HTTP request.
1. The function **authenticates with Google Cloud**.
2. It sends a **request to Cloud Run Jobs API** to start the scraper.
3. **If successful**, it returns `"Scraper executed successfully"`.
4. **If an error occurs**, it returns the error message.

# Features:

Automated Web Scraping using Selenium.

Data Processing with Pandas (word count, character count, etc.).

BigQuery Integration for structured storage.

Dockerized Deployment for portability.

Google Cloud Run Support for cloud execution.

# Deployment prerequisites

Before running the project, ensure you have the following installed:

Docker & Docker Compose

Google Cloud SDK (gcloud CLI) with authentication configured

Google Cloud Project with BigQuery API enabled

Service Account Key (JSON file for BigQuery authentication) IMPORTANT: The deployment will not work since it uses my personal google cloud key to authenticate, but this can be easily configured!

# Running the Bash Deployment Script

First git clone the repo

To deploy the scraper to Google Cloud Run, use the provided deploy.sh script.

-Set the Execution Permission

chmod +x deploy.sh

-Deploy the Service

./deploy.sh
