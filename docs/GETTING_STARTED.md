# Getting Started Guide

## Prerequisites

- Python 3.8+
- CUDA 11.0+ (optional, for GPU acceleration)
- PostgreSQL 12+ or MongoDB
- 8GB RAM minimum (16GB recommended)
- 10GB+ disk space for models and data

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/traffic-violation-detection.git
cd traffic-violation-detection
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
# - Database credentials
# - API keys
# - Email/SMS configuration
```

### 5. Download Datasets (Optional)

```bash
# Get dataset download guide
python scripts/download_datasets.py --guide

# Or download sample models
python scripts/download_datasets.py --download-models
```

---

## Quick Start

### Run Backend API

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit: http://localhost:8000/api/docs

### Run Dashboard

```bash
streamlit run frontend/streamlit_app/app.py
```

Visit: http://localhost:8501

---

## Training Models

### Train Helmet Detection Model

```bash
python scripts/train_helmet_model.py \
  --data data/helmet \
  --epochs 100 \
  --batch-size 16 \
  --img-size 640
```

### Train Plate Detection Model

```bash
python scripts/train_plate_model.py \
  --data data/number_plate \
  --epochs 80 \
  --batch-size 16
```

---

## Docker Deployment

### Build & Run with Docker Compose

```bash
# Build images
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

Services:

- API: http://localhost:8000
- Dashboard: http://localhost:8501
- Database: localhost:5432

---

## Database Setup

### PostgreSQL

```bash
# Create database
createdb traffic_violations

# Run migrations
python -c "from backend.app.database.database import init_db; init_db()"
```

### MongoDB (Alternative)

```bash
# Update config to use MongoDB
# In .env: DB_TYPE=mongodb
# In config/config.yaml: DATABASE.TYPE: mongodb
```

---

## Processing Images/Videos

### Process Single Image

```bash
python -c "
from backend.app.services.complete_pipeline import CompletePipeline

pipeline = CompletePipeline(
    helmet_model_path='models/helmet_detection/best.pt',
    plate_model_path='models/plate_detection/best.pt'
)

results = pipeline.process_image(
    image_path='test_image.jpg',
    latitude=28.7041,
    longitude=77.1025,
    location_name='Test Location'
)

print(f'Violations found: {results[\"violations_found\"]}')"
```

### Process Video File

```bash
python backend/app/services/complete_pipeline.py \
  --video input_video.mp4 \
  --latitude 28.7041 \
  --longitude 77.1025 \
  --location "NH-48 Toll" \
  --output output_video.mp4 \
  --auto-challan
```

### Process RTSP Stream

```python
from backend.app.services.complete_pipeline import CompletePipeline

pipeline = CompletePipeline(
    helmet_model_path='models/helmet_detection/best.pt',
    plate_model_path='models/plate_detection/best.pt',
    auto_issue_challan=True
)

stats = pipeline.process_rtsp_stream(
    rtsp_url='rtsp://camera-ip:554/stream',
    latitude=28.7041,
    longitude=77.1025,
    location_name='Traffic Junction',
    duration_seconds=3600  # 1 hour
)
```

---

## Testing

### Run Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=backend tests/

# Run specific test
pytest tests/test_helmet_detection.py -v
```

---

## API Usage

### Using cURL

```bash
# Detect violations from image
curl -X POST "http://localhost:8000/api/violations/detect" \
  -F "file=@image.jpg" \
  -F "latitude=28.7041" \
  -F "longitude=77.1025" \
  -F "location_name=NH-48 Toll"

# List violations
curl "http://localhost:8000/api/violations/list?limit=10"

# Get heatmap data
curl "http://localhost:8000/api/analytics/heatmap/data?days=7"
```

### Using Python

```python
import requests

API_URL = "http://localhost:8000/api"

# Detect violation
with open("image.jpg", "rb") as f:
    resp = requests.post(
        f"{API_URL}/violations/detect",
        files={"file": f},
        data={
            "latitude": 28.7041,
            "longitude": 77.1025,
            "location_name": "NH-48 Toll"
        }
    )
    print(resp.json())

# Issue challan
resp = requests.post(
    f"{API_URL}/challan/issue",
    json={
        "violation_id": 1,
        "owner_name": "John Doe",
        "owner_phone": "+919876543210",
        "owner_email": "john@example.com",
        "registration_number": "DL-01AB1234"
    }
)
print(resp.json())
```

---

## Configuration

### Model Settings

Edit `config/config.yaml`:

```yaml
DETECTION:
  HELMET:
    CONFIDENCE_THRESHOLD: 0.5
    IOU_THRESHOLD: 0.45
    MODEL_INPUT_SIZE: 640

VIOLATIONS:
  HELMET_NOT_WORN:
    PENALTY_AMOUNT: 500
```

### Database

Edit `.env`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=traffic_violations
```

---

## Troubleshooting

### CUDA/GPU Issues

```bash
# Check if CUDA is available
python -c "import torch; print(torch.cuda.is_available())"

# If False, models will use CPU (slower)
# To install CUDA-enabled PyTorch:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Database Connection Error

```bash
# Check if PostgreSQL is running
psql -U postgres -d traffic_violations

# If not installed, install PostgreSQL:
# Windows: https://www.postgresql.org/download/windows/
# macOS: brew install postgresql
# Linux: sudo apt-get install postgresql
```

### Model Loading Issues

```bash
# Ensure models exist in correct path
ls models/helmet_detection/
ls models/plate_detection/

# Download models if missing
python scripts/download_datasets.py --download-models
```

### RTSP Stream Connection Issues

```bash
# Test RTSP URL connectivity
ffmpeg -rtsp_transport tcp -i rtsp://camera-ip:554/stream -f null -

# Ensure camera/NVR is accessible and streaming
```

---

## Performance Optimization

### For Production

```python
# Use GPU
detector = HelmetDetector(
    model_path="models/helmet_detection/best.pt",
    device="cuda"
)

# Increase batch size for video processing
# in complete_pipeline.py
```

### For Edge Devices (Jetson Nano)

```bash
# Install optimized dependencies
pip install torch==1.13.0 torchvision==0.14.0 -f https://download.pytorch.org/whl/torch_stable.html

# Use smaller model variants
# YOLOv8n (nano) instead of YOLOv8m (medium)
```

---

## Next Steps

1. **Download/Prepare Datasets** - See `scripts/download_datasets.py`
2. **Train Models** - See [Training Guide](TRAINING.md)
3. **Deploy API** - See [Deployment Guide](DEPLOYMENT.md)
4. **Monitor Performance** - Use dashboard and logs
5. **Publish Research** - See [Paper Outline](../research_paper/PAPER_OUTLINE.md)

---

## Support

- 📖 [Full Documentation](https://docs.example.com)
- 🐛 [Report Issues](https://github.com/yourusername/traffic-violation-detection/issues)
- 💬 [Discussions](https://github.com/yourusername/traffic-violation-detection/discussions)
- 📧 [Contact](mailto:support@example.com)
