# Deploy to Google Cloud Platform

## Option 1: Google Cloud Run (Recommended - Serverless)

### Prerequisites
- Google Cloud Account
- Google Cloud CLI installed
- Docker installed locally

### Step 1: Create GCP Project
```bash
# Set your project
gcloud config set project YOUR_PROJECT_ID
gcloud auth login
```

### Step 2: Build and Push Docker Image
```bash
# Build Docker image
docker build -t gcr.io/YOUR_PROJECT_ID/traffic-violation:latest .

# Push to Google Container Registry
docker push gcr.io/YOUR_PROJECT_ID/traffic-violation:latest
```

### Step 3: Deploy to Cloud Run
```bash
gcloud run deploy traffic-violation \
  --image gcr.io/YOUR_PROJECT_ID/traffic-violation:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8001 \
  --memory 2Gi \
  --cpu 2 \
  --timeout 3600 \
  --max-instances 10
```

### Step 4: Access Your Application
After deployment, you'll get a URL like:
```
https://traffic-violation-XXXX-uc.a.run.app
```

Access: `https://traffic-violation-XXXX-uc.a.run.app/webcam`

---

## Option 2: Google App Engine

### Step 1: Create app.yaml
```yaml
runtime: python39
env: standard
instance_class: F2

env_variables:
  LOG_LEVEL: "INFO"

handlers:
- url: /.*
  script: auto
  
automatic_scaling:
  min_instances: 1
  max_instances: 5
```

### Step 2: Deploy
```bash
gcloud app deploy
```

---

## Option 3: Google Compute Engine (VM)

### Step 1: Create VM Instance
```bash
gcloud compute instances create traffic-detection-vm \
  --image-family ubuntu-2004-lts \
  --image-project ubuntu-os-cloud \
  --machine-type n1-standard-2 \
  --zone us-central1-a
```

### Step 2: SSH into VM
```bash
gcloud compute ssh traffic-detection-vm --zone us-central1-a
```

### Step 3: Install and Run
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3.9 python3-pip -y

# Clone/copy your code
# Install requirements
pip3 install -r requirements.txt

# Run with systemd (for auto-restart)
sudo systemctl start traffic-violation
sudo systemctl enable traffic-violation
```

---

## Important Considerations for Cloud Deployment

### ⚠️ Camera Limitation
- **Local camera (cv2.VideoCapture) won't work in cloud**
- **Solution**: 
  1. Use mock detection (currently enabled) ✅
  2. Accept uploaded images instead
  3. Use cloud cameras/RTSP streams

### 📁 File Storage
- Local disk storage doesn't persist in Cloud Run
- **Solution**: Use Google Cloud Storage
  ```python
  from google.cloud import storage
  
  bucket = storage.Client().bucket('your-bucket')
  blob = bucket.blob('evidence/' + filename)
  blob.upload_from_filename(filepath)
  ```

### 🗄️ Database
- Currently no database (mock mode)
- **For production**:
  ```bash
  # Use Cloud SQL
  gcloud sql instances create traffic-db \
    --database-version POSTGRES_13 \
    --tier db-f1-micro
  ```

---

## Deploy Using Cloud Run (Quickest Option)

### Full Command Sequence
```bash
# 1. Authenticate
gcloud auth login

# 2. Set project
gcloud config set project YOUR_PROJECT_ID

# 3. Build
docker build -t gcr.io/YOUR_PROJECT_ID/traffic-violation:latest .

# 4. Push
docker push gcr.io/YOUR_PROJECT_ID/traffic-violation:latest

# 5. Deploy
gcloud run deploy traffic-violation \
  --image gcr.io/YOUR_PROJECT_ID/traffic-violation:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8001 \
  --memory 2Gi \
  --timeout 3600

# 6. View logs
gcloud run logs read traffic-violation
```

---

## Cost Estimation (Google Cloud Run)

| Resource | Free Tier | Pricing |
|----------|-----------|---------|
| vCPU | 180,000 vCPU-seconds/month | $0.000024/vCPU-second |
| Memory | 360,000 GB-seconds/month | $0.0000025/GB-second |
| Requests | 2 million/month | $0.40/million requests |

**Estimated Monthly Cost**: ~$5-20 for low traffic

---

## Monitoring & Logging

```bash
# View logs
gcloud run logs read traffic-violation --region us-central1

# Monitor metrics
gcloud monitoring metrics-descriptors list

# Set up alerts
gcloud alpha monitoring policies create \
  --notification-channels=CHANNEL_ID
```

---

## Environment Variables (Cloud Run)

Set via console or CLI:
```bash
gcloud run deploy traffic-violation \
  --set-env-vars LOG_LEVEL=INFO,DATABASE_URL=postgresql://... \
  ...
```

---

## Troubleshooting

**Service not starting?**
```bash
gcloud run logs read traffic-violation --limit 50
```

**Permission denied?**
```bash
# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

**Port issues?**
- Cloud Run only accepts port 8080 or 443
- Our app is configured for 8001 internally ✅

---

## Summary

✅ **Fastest**: Google Cloud Run (5 mins)
✅ **Cheapest**: Cloud Run with free tier
✅ **Easiest**: App Engine (no Docker needed)
✅ **Most Control**: Compute Engine (VM)

**Recommended**: Start with **Cloud Run** for quick deployment!
