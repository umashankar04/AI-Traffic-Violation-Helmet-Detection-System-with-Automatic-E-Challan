# 🚨 AI Traffic Violation & Helmet Detection System with Automatic E-Challan

> **Smart Vision-based Traffic Violation Detection using Deep Learning & OCR**

An intelligent, end-to-end AI system that automatically detects traffic violations (helmet violations, signal jumping, triple riding), extracts vehicle number plates using OCR, and issues automated E-challans with geo-tagged violation heatmap analytics.

---

## 🎯 Features

✅ **Real-time Helmet Detection** - YOLOv8-based helmet/no-helmet classification  
✅ **Number Plate Recognition** - YOLO + EasyOCR/Tesseract with Indian format validation  
✅ **Automatic E-Challan Issuance** - REST API-driven violation documentation  
✅ **Violation Heatmap Analytics** - Geo-spatial visualization of accident-prone zones  
✅ **Live RTSP Stream Processing** - Real-world CCTV/camera feed integration  
✅ **Streamlit Dashboard** - Real-time monitoring and analytics UI  
✅ **Scalable Backend** - FastAPI with async processing  
✅ **Production-Ready** - Docker support, logging, error handling

---

## 📊 System Architecture

```
CCTV/Video Feed
      ↓
Frame Extraction & Preprocessing
      ↓
YOLOv8 Helmet Detection (Person Detection)
      ↓
YOLOv8 Number Plate Detection
      ↓
EasyOCR/Tesseract (Plate Text Extraction)
      ↓
Violation Rule Engine
      ↓
Database & E-Challan API
      ↓
Heatmap + Dashboard
      ↓
Admin Portal / Traffic Authority Portal
```

---

## 🛠️ Tech Stack

| Component         | Technology                    |
| ----------------- | ----------------------------- |
| **Detection**     | YOLOv8/YOLOv9, PyTorch        |
| **OCR**           | EasyOCR, Tesseract, PaddleOCR |
| **Backend**       | FastAPI, SQLAlchemy           |
| **Database**      | PostgreSQL, MongoDB           |
| **Frontend**      | Streamlit, Folium, Plotly     |
| **Deployment**    | Docker, Docker-Compose        |
| **Cloud Storage** | AWS S3 / Azure Blob           |

---

## 📁 Project Structure

```
traffic-violation-detection/
├── config/
│   ├── config.yaml              # Main configuration file
│   └── logging.yaml
├── data/
│   ├── helmet/                  # Helmet detection dataset
│   ├── number_plate/            # Number plate dataset
│   ├── raw/                     # Raw video/images
│   └── evidence/                # Violation evidence images
├── models/
│   ├── helmet_detection/        # Trained helmet model
│   ├── plate_detection/         # Trained plate detection model
│   └── ocr/                     # OCR models
├── backend/
│   ├── app/
│   │   ├── routes/              # API endpoints
│   │   ├── models/              # Database models
│   │   ├── services/            # Business logic
│   │   ├── database/            # DB connections
│   │   └── main.py              # FastAPI app
│   └── requirements.txt
├── frontend/
│   ├── streamlit_app/           # Dashboard code
│   ├── pages/                   # Multi-page UI
│   └── components/              # Reusable components
├── scripts/
│   ├── train_helmet_model.py    # Training script
│   ├── train_plate_model.py
│   ├── download_datasets.py
│   └── process_video.py
├── notebooks/
│   ├── helmet_detection.ipynb
│   ├── plate_ocr.ipynb
│   └── analysis.ipynb
├── research_paper/
│   ├── paper.tex
│   ├── sections/
│   └── images/
├── tests/
│   ├── test_helmet_detection.py
│   ├── test_ocr.py
│   └── test_api.py
├── logs/                        # Application logs
├── .env.example                 # Environment variables template
├── .gitignore
├── requirements.txt             # Python dependencies
├── setup.py
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- CUDA 11.0+ (for GPU acceleration) - Optional but recommended
- PostgreSQL 12+ or MongoDB

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/traffic-violation-detection.git
cd traffic-violation-detection
```

2. **Create virtual environment**

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Setup configuration**

```bash
cp .env.example .env
# Edit .env with your settings
```

5. **Download pre-trained models** (Optional)

```bash
python scripts/download_models.py
```

---

## 📦 Phases & Implementation

### Phase 1: Helmet Detection

```bash
python scripts/train_helmet_model.py \
  --data data/helmet \
  --epochs 100 \
  --batch-size 16 \
  --img-size 640
```

### Phase 2: Number Plate OCR

```bash
python scripts/train_plate_model.py \
  --data data/number_plate \
  --epochs 80 \
  --batch-size 16
```

### Phase 3-4: Run Detection Pipeline

```bash
python backend/app/main.py
```

### Phase 5: Launch Dashboard

```bash
streamlit run frontend/streamlit_app/app.py
```

---

## 🎓 Research Paper

Complete research paper template with sections for:

- Abstract & Introduction
- Literature Review
- Methodology & Architecture
- Implementation Details
- Results & Analysis
- Heatmap-based Violation Study
- Conclusion & Future Scope

📄 See `research_paper/README.md` for detailed structure.

---

## 📊 Expected Performance

| Metric                    | Target    |
| ------------------------- | --------- |
| Helmet Detection Accuracy | 92-98%    |
| Number Plate Detection    | 90-96%    |
| OCR Recognition Rate      | 85-95%    |
| Real-time FPS             | 15-30 FPS |
| False Positive Rate       | <2%       |

---

## 🔗 API Endpoints

### Violation Detection

- `POST /api/violations/detect` - Detect violation from image/video
- `GET /api/violations/list` - Get all violations
- `GET /api/violations/{id}` - Get violation details

### E-Challan

- `POST /api/challan/issue` - Issue new E-challan
- `GET /api/challan/{id}` - Get challan details
- `PUT /api/challan/{id}/status` - Update challan status

### Analytics

- `GET /api/heatmap/data` - Get heatmap violation data
- `GET /api/analytics/summary` - Get summary stats
- `GET /api/analytics/trends` - Get violation trends

---

## 🐳 Docker Deployment

```bash
# Build & run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

---

## 📝 Configuration Guide

Edit `config/config.yaml` to customize:

- Model paths & confidence thresholds
- Violation rules & penalties
- Database credentials
- Email/SMS notification settings
- Heatmap parameters

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=backend tests/

# Run specific test
pytest tests/test_helmet_detection.py -v
```

---

## 📚 Documentation

- [API Documentation](docs/API.md)
- [Model Training Guide](docs/TRAINING.md)
- [Database Schema](docs/DATABASE.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

---

## 🔮 Future Enhancements

- [ ] Signal jumping detection
- [ ] Vehicle speed estimation using optical flow
- [ ] Triple riding detection
- [ ] Vehicle type classification (bike/car/truck)
- [ ] Integration with Police RTO Vehicle Database
- [ ] Drone-based monitoring
- [ ] Mobile app for challans
- [ ] Payment gateway integration

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

---

## 👥 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📞 Contact & Support

- **Email**: your.email@example.com
- **GitHub Issues**: [Report a bug](https://github.com/yourusername/traffic-violation-detection/issues)
- **Discussions**: [Join our community](https://github.com/yourusername/traffic-violation-detection/discussions)

---

## 🙏 Acknowledgments

- YOLOv8 by Ultralytics
- EasyOCR contributors
- OpenCV community
- Streamlit team
- All dataset contributors

---

**Made with ❤️ for Safer Roads**
