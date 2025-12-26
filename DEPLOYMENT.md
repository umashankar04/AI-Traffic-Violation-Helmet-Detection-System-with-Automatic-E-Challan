# Free & Open-Source Deployment Guide

This guide shows how to deploy the Traffic Violation Detection System **for free** using various platforms.

## Table of Contents

1. [Google Cloud Run (Free Tier)](#google-cloud-run)
2. [Heroku (Free - Limited)](#heroku)
3. [Railway.app](#railway)
4. [Render](#render)
5. [DigitalOcean App Platform](#digitalocean)
6. [Self-Hosted (Free)](#self-hosted)

---

## Google Cloud Run

**Cost**: FREE for first 2 million requests/month, then $0.40 per million

### Setup

1. **Create Google Cloud Account** (Free tier)
   - Go to: https://cloud.google.com/free
   - Sign up with email

2. **Install Google Cloud SDK**
   ```bash
   # Windows: Download installer from https://cloud.google.com/sdk/docs/install
   # macOS:
   brew install google-cloud-sdk
   # Linux: https://cloud.google.com/sdk/docs/install
   ```

3. **Deploy Using Script**
   ```powershell
   # Windows
   .\deploy_to_google_cloud.bat
   
   # Linux/macOS
   bash deploy_to_google_cloud.sh
   ```

4. **Manual Deployment**
   ```bash
   # Authenticate
   gcloud auth login
   gcloud config set project YOUR-PROJECT-ID
   
   # Build & deploy
   gcloud run deploy traffic-violation \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --memory 2Gi \
     --cpu 2
   ```

**Access**: `https://traffic-violation-XXXXX.run.app/webcam`

**Advantages**:
- ✅ Free tier covers most use cases
- ✅ Auto-scaling
- ✅ HTTPS included
- ✅ Easy deployment

**Limitations**:
- ⚠️ No local camera access
- ⚠️ Requires Google account
- ⚠️ Paid after free tier

---

## Heroku

**Cost**: FREE plan REMOVED (but still good for learning)

### Alternative: Use Heroku with free database

```bash
# Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Create app
heroku create traffic-violation-app

# Deploy
git push heroku main

# Open app
heroku open
```

---

## Railway.app

**Cost**: $5/month free credit (Good for small projects)

### Setup

1. **Go to**: https://railway.app
2. **Sign up** with GitHub
3. **Connect repo**: Select your GitHub repository
4. **Add Service**: Choose Python
5. **Deploy**: Auto-deploys on push to main

```bash
# Local setup
npm install -g @railway/cli
railway login
railway up
```

**Access**: `https://[project-name].up.railway.app/webcam`

---

## Render

**Cost**: FREE tier available (limited resources)

### Setup

1. **Go to**: https://render.com
2. **Sign up** with GitHub
3. **Create Web Service**:
   - Connect GitHub repo
   - Choose Python
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`

4. **Deploy**: Automatic on push

**Access**: `https://traffic-violation-XXXXX.onrender.com/webcam`

**Limitations**:
- Free tier has limited resources
- Spins down after 15 minutes of inactivity

---

## DigitalOcean App Platform

**Cost**: $5/month (or $12/month for better specs)

### Setup

1. **Create DigitalOcean Account**: https://www.digitalocean.com
2. **Create App Platform App**:
   - Connect GitHub repo
   - Select Python runtime
   - Configure build command
   - Deploy

```bash
# Install doctl CLI
# https://docs.digitalocean.com/reference/doctl/how-to/install/

doctl apps create --spec app.yaml
```

**app.yaml**:
```yaml
name: traffic-violation
services:
- name: api
  github:
    repo: yourusername/traffic-violation-detection
    branch: main
  build_command: pip install -r requirements.txt
  run_command: uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
  http_port: 8000
  envs:
  - key: PYTHON_VERSION
    value: "3.10"
```

---

## Self-Hosted (Completely Free)

### Option 1: Home Server

```bash
# Requirements:
# - Old laptop/Raspberry Pi
# - 24/7 internet connection
# - Port forwarding enabled

# Run on Raspberry Pi
python -m uvicorn backend.app.main:app \
  --host 0.0.0.0 \
  --port 8001 \
  --workers 4

# Access: http://your-home-ip:8001/webcam
```

### Option 2: Use ngrok for Remote Access

```bash
# Install ngrok: https://ngrok.com

# Run server
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8001

# In another terminal
ngrok http 8001

# Access: https://[unique-id].ngrok.io/webcam
```

### Option 3: Docker on Home Server

```bash
docker build -t traffic-violation .

docker run -d \
  -p 8001:8001 \
  --name traffic-violation \
  traffic-violation

# Access: http://home-ip:8001/webcam
```

---

## Comparison Table

| Platform | Cost | Ease | Scalability | Uptime |
|----------|------|------|-------------|--------|
| Google Cloud Run | Free (2M req) | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Railway | $5/mo | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Render | Free | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| DigitalOcean | $5/mo | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Home Server | Free | ⭐⭐ | ⭐ | ⭐⭐ |
| ngrok | Free | ⭐⭐⭐⭐ | ⭐ | ⭐ |

---

## Environment Variables by Platform

### Google Cloud Run
```bash
gcloud run deploy traffic-violation \
  --set-env-vars API_HOST=0.0.0.0,API_PORT=8001,DEBUG=False
```

### Railway/Render
Add in platform settings:
```
API_HOST=0.0.0.0
API_PORT=8001
DEBUG=False
```

### Home Server
Create `.env` file:
```
API_HOST=0.0.0.0
API_PORT=8001
DEBUG=True
```

---

## Domain Setup (Optional)

### Free Domain Options
- Freenom: https://www.freenom.com (free .tk domains)
- Cloudflare: Free DNS only

### Custom Domain on Google Cloud Run

```bash
gcloud run deploy traffic-violation \
  --region us-central1 \
  --update-custom-domains traffic-violation.example.com
```

---

## Monitoring & Logs

### Google Cloud Run
```bash
gcloud run logs read traffic-violation --limit 50
```

### Railway
```bash
railway logs
```

### Render
Check dashboard at: https://dashboard.render.com

### Local
```bash
tail -f logs/app.log
```

---

## Database Setup (Free Options)

### PostgreSQL (Free)

**Railway + PostgreSQL**:
1. Create Railway project
2. Add PostgreSQL plugin
3. Use connection string from Railway

**DigitalOcean Managed Database**:
- $15/month for PostgreSQL

**Local SQLite** (included):
- No setup needed
- File-based at `database.db`

**Neon.tech** (Free PostgreSQL):
```bash
# Sign up: https://neon.tech
# Get connection string
# Add to .env:
DATABASE_URL=postgresql://user:password@localhost/traffic_db
```

---

## Troubleshooting

### 404 on /webcam
```bash
# Check if frontend/html/index.html exists
ls -la frontend/html/

# Redeploy
gcloud run deploy traffic-violation --source .
```

### Port Already in Use
```bash
# Find process on port 8001
lsof -i :8001
kill -9 [PID]
```

### Camera Not Working in Cloud
```bash
# Cloud doesn't have camera access
# System uses mock detection automatically
# Check logs for: "Using mock detector"
```

### Deployment Fails
```bash
# Check logs
gcloud run logs read traffic-violation --limit 100

# Try local build first
docker build -t traffic-violation .
docker run -p 8001:8001 traffic-violation
```

---

## Cost Breakdown (Monthly Estimate)

**Google Cloud Run**: $0-5/month
- First 2M requests: FREE
- Compute: ~$0.00002 per request

**Railway**: $5/month
- Base credit: $5

**Render**: FREE (limited)
- Better tier: $12/month

**DigitalOcean**: $5/month
- App platform: $5/month

**Home Server**: $0/month
- Only electricity cost (~$5-10)

---

## Production Best Practices

### Secrets Management
```bash
# Google Cloud
gcloud secrets create api-key --data-file=-
gcloud run deploy traffic-violation \
  --set-env-vars API_KEY=secret:api-key:latest

# Railway
railway variable set API_KEY=your-key

# Environment file (.env)
API_KEY=secret-key-here
DATABASE_URL=postgresql://...
```

### Logging
```python
import logging

logger = logging.getLogger(__name__)
logger.info("Server started")
logger.error(f"Error: {e}")
```

### Health Checks
```bash
curl http://localhost:8001/health
# Response: {"status": "healthy"}
```

---

**Choose the platform that best fits your needs and budget!** 🚀

For questions, open an issue on GitHub.
