#!/bin/bash

# Variables
PROJECT_ID="pythonscraper-453902"
REGION="us-central1"
REPO_NAME="scraper-repo"
IMAGE_NAME="scraper-image"
SERVICE_NAME="scraper-service"

# Authenticate with Google Cloud
gcloud auth login
gcloud config set project $PROJECT_ID

# Enable necessary services
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com

# Build the Docker image
docker build -t $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME .

# Push the image to Google Artifact Registry
docker push $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME

# Deploy the container to Cloud Run
gcloud run jobs create $JOB_NAME \
    --image $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME \
    --region $REGION \
    --task-timeout=600s \
    --memory=512Mi \
    --cpu=1

echo "Deployment completed! Cloud Run URL:"
gcloud run services describe $SERVICE_NAME --platform managed --region $REGION --format='value(status.url)'
