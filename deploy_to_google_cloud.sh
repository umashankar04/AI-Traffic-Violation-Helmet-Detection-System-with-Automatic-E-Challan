#!/bin/bash

# Google Cloud Deployment Script
# This script deploys the Traffic Violation Detection System to Google Cloud Run

set -e

echo "======================================"
echo "Traffic Violation Detection System"
echo "Google Cloud Deployment Script"
echo "======================================"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "ERROR: gcloud CLI is not installed. Please install it first."
    echo "Download from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed. Please install it first."
    exit 1
fi

# Get project ID
read -p "Enter your Google Cloud Project ID: " PROJECT_ID
read -p "Enter deployment region (default: us-central1): " REGION
REGION=${REGION:-us-central1}

# Set project
echo "Setting GCP project to: $PROJECT_ID"
gcloud config set project $PROJECT_ID

# Authenticate if needed
echo "Authenticating with Google Cloud..."
gcloud auth login

# Enable required APIs
echo "Enabling required APIs..."
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build Docker image
echo "Building Docker image..."
docker build -t gcr.io/$PROJECT_ID/traffic-violation:latest .

# Push to Container Registry
echo "Pushing image to Google Container Registry..."
docker push gcr.io/$PROJECT_ID/traffic-violation:latest

# Deploy to Cloud Run
echo "Deploying to Google Cloud Run..."
gcloud run deploy traffic-violation \
  --image gcr.io/$PROJECT_ID/traffic-violation:latest \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8001 \
  --memory 2Gi \
  --cpu 2 \
  --timeout 3600 \
  --max-instances 10

echo ""
echo "======================================"
echo "Deployment Complete!"
echo "======================================"
echo ""
echo "Your application is now deployed to Google Cloud Run"
echo "Check the URL above to access your application"
echo ""
echo "View logs:"
echo "  gcloud run logs read traffic-violation --region $REGION"
echo ""
echo "Visit your app:"
echo "  https://traffic-violation-XXX-$REGION.a.run.app/webcam"
echo ""
