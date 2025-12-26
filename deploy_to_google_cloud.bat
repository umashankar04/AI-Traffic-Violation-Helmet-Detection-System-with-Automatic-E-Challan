@echo off
REM Google Cloud Deployment Script for Windows
REM This script deploys the Traffic Violation Detection System to Google Cloud Run

setlocal enabledelayedexpansion

echo ======================================
echo Traffic Violation Detection System
echo Google Cloud Deployment Script (Windows)
echo ======================================
echo.

REM Check if gcloud is installed
where gcloud >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: gcloud CLI is not installed.
    echo Download from: https://cloud.google.com/sdk/docs/install
    pause
    exit /b 1
)

REM Check if docker is installed
where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Docker is not installed.
    pause
    exit /b 1
)

REM Get project ID
set /p PROJECT_ID="Enter your Google Cloud Project ID: "
set /p REGION="Enter deployment region (default: us-central1): "
if "!REGION!"=="" set REGION=us-central1

echo.
echo Setting GCP project to: !PROJECT_ID!
gcloud config set project !PROJECT_ID!

echo Authenticating with Google Cloud...
gcloud auth login

echo.
echo Enabling required APIs...
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

echo.
echo Building Docker image...
docker build -t gcr.io/!PROJECT_ID!/traffic-violation:latest .

echo.
echo Pushing image to Google Container Registry...
docker push gcr.io/!PROJECT_ID!/traffic-violation:latest

echo.
echo Deploying to Google Cloud Run...
gcloud run deploy traffic-violation ^
  --image gcr.io/!PROJECT_ID!/traffic-violation:latest ^
  --platform managed ^
  --region !REGION! ^
  --allow-unauthenticated ^
  --port 8001 ^
  --memory 2Gi ^
  --cpu 2 ^
  --timeout 3600 ^
  --max-instances 10

echo.
echo ======================================
echo Deployment Complete!
echo ======================================
echo.
echo Your application is now deployed to Google Cloud Run
echo.
echo View logs:
echo   gcloud run logs read traffic-violation --region !REGION!
echo.
echo To access your app, look for the Service URL above
echo.
pause
