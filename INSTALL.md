# Installation Guide

Complete step-by-step guide to install and run the Traffic Violation Detection System.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Windows Installation](#windows-installation)
3. [macOS Installation](#macos-installation)
4. [Linux Installation](#linux-installation)
5. [Docker Installation](#docker-installation)
6. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements
- **OS**: Windows 10+, macOS 10.14+, Ubuntu 18.04+
- **Python**: 3.9 or higher
- **RAM**: 2 GB
- **Disk**: 500 MB
- **Webcam**: Optional (works with mock mode)
- **Internet**: Required for initial setup

### Recommended Requirements
- **OS**: Windows 11, macOS 12+, Ubuntu 22.04+
- **Python**: 3.10 or higher
- **RAM**: 4 GB+
- **Disk**: 2 GB
- **GPU**: NVIDIA GPU for faster processing (optional)
- **Internet**: 5+ Mbps

### Check Your System

**Python Version**:
```bash
python --version
# Should show 3.9+
```

**pip Version**:
```bash
pip --version
```

---

## Windows Installation

### Step 1: Install Python

1. Download Python from: https://www.python.org/downloads/
2. **Important**: Check "Add Python to PATH" during installation
3. Click "Install Now"
4. Verify installation:
   ```bash
   python --version
   ```

### Step 2: Clone Repository

```bash
# Open Command Prompt or PowerShell
git clone https://github.com/yourusername/traffic-violation-detection.git
cd traffic-violation-detection
```

### Step 3: Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 5: Run Application

```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8001
```

### Step 6: Access Web Interface

Open browser to: **http://127.0.0.1:8001/webcam**

---

## macOS Installation

### Step 1: Install Python

```bash
# Using Homebrew (recommended)
brew install python@3.10

# Or download from: https://www.python.org/downloads/
```

### Step 2: Install Git (if not installed)

```bash
brew install git
```

### Step 3: Clone Repository

```bash
git clone https://github.com/yourusername/traffic-violation-detection.git
cd traffic-violation-detection
```

### Step 4: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 5: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 6: Grant Camera Permission (Important!)

1. Go to **System Preferences** → **Security & Privacy** → **Camera**
2. Add Terminal/IDE to allowed apps

### Step 7: Run Application

```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8001
```

### Step 8: Access Web Interface

Open browser to: **http://127.0.0.1:8001/webcam**

---

## Linux Installation

### Step 1: Update System

**Ubuntu/Debian**:
```bash
sudo apt-get update
sudo apt-get upgrade -y
```

**Fedora/RedHat**:
```bash
sudo dnf update -y
```

### Step 2: Install Python & Dependencies

**Ubuntu/Debian**:
```bash
sudo apt-get install -y python3.10 python3.10-venv python3-pip git
sudo apt-get install -y libsm6 libxext6 libxrender-dev libgomp1
```

**Fedora**:
```bash
sudo dnf install -y python3.10 python3-pip git
sudo dnf install -y libSM libXext libXrender libgomp
```

### Step 3: Clone Repository

```bash
git clone https://github.com/yourusername/traffic-violation-detection.git
cd traffic-violation-detection
```

### Step 4: Create Virtual Environment

```bash
python3.10 -m venv venv
source venv/bin/activate
```

### Step 5: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 6: Install Camera Support (Optional)

```bash
# For USB cameras
sudo apt-get install -y v4l-utils

# Check available cameras
ls -la /dev/video*
```

### Step 7: Run Application

```bash
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8001
```

### Step 8: Access Web Interface

Open browser to: **http://localhost:8001/webcam**

Or from another machine: **http://[your-ip]:8001/webcam**

---

## Docker Installation

### Step 1: Install Docker

- **Windows**: https://www.docker.com/products/docker-desktop
- **macOS**: https://www.docker.com/products/docker-desktop
- **Linux**: 
  ```bash
  curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  ```

### Step 2: Clone Repository

```bash
git clone https://github.com/yourusername/traffic-violation-detection.git
cd traffic-violation-detection
```

### Step 3: Build Docker Image

```bash
docker build -t traffic-violation:latest .
```

### Step 4: Run Container

**Basic**:
```bash
docker run -p 8001:8001 \
  --name traffic-violation \
  traffic-violation:latest
```

**With Camera Access** (Linux):
```bash
docker run -p 8001:8001 \
  --device /dev/video0 \
  --name traffic-violation \
  traffic-violation:latest
```

**With Volume Mount** (for persistence):
```bash
docker run -p 8001:8001 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/logs:/app/logs \
  --name traffic-violation \
  traffic-violation:latest
```

### Step 5: Access Application

Open browser to: **http://localhost:8001/webcam**

### Step 6: View Logs

```bash
docker logs traffic-violation
```

### Step 7: Stop Container

```bash
docker stop traffic-violation
docker rm traffic-violation
```

---

## Troubleshooting

### Issue: "python: command not found"

**Solution**:
```bash
# Windows: Add Python to PATH in System Environment Variables
# macOS: Use python3 instead of python
python3 --version

# Linux: Install Python
sudo apt-get install python3.10
```

### Issue: "ModuleNotFoundError: No module named 'cv2'"

**Solution**:
```bash
pip install --upgrade opencv-python==4.8.1.78
pip install numpy==1.26.4
```

### Issue: "Port 8001 already in use"

**Windows**:
```powershell
netstat -ano | findstr :8001
taskkill /PID [PID] /F
```

**macOS/Linux**:
```bash
lsof -i :8001
kill -9 [PID]
```

### Issue: Camera not opening

**Windows**:
- Check Device Manager → Cameras
- Restart IDE with admin privileges
- Run: `python test_camera.py`

**macOS**:
- System Preferences → Security & Privacy → Camera → Allow your app

**Linux**:
```bash
# Check camera
v4l2-ctl --list-devices

# Test camera
python test_camera.py
```

### Issue: Virtual environment not activating

**Windows**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\activate
```

**macOS/Linux**:
```bash
chmod +x venv/bin/activate
source venv/bin/activate
```

### Issue: Permission Denied Error

**Linux**:
```bash
# Run with sudo
sudo python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8001

# Or add to sudoers (not recommended)
```

### Issue: "Address already in use" with Docker

```bash
# Find and remove old container
docker ps -a
docker rm [container-id]

# Or use different port
docker run -p 8002:8001 traffic-violation:latest
```

### Issue: Low Performance / Slow Detection

**Solutions**:
1. Use GPU: `pip install torch torchvision`
2. Reduce frame resolution
3. Increase workers: `--workers 4`
4. Enable mock mode (automatic if models unavailable)

---

## Verify Installation

Run the test script:

```bash
python test_camera.py
```

Expected output:
```
✓ Camera opened successfully
✓ Frame captured: (1280, 720)
✓ Frame saved to: data/evidence/test_frame.jpg
✓ Camera test passed!
```

---

## Next Steps

1. **Try the web interface**: http://127.0.0.1:8001/webcam
2. **Read the README**: See detailed features and API docs
3. **Explore deployment**: See DEPLOYMENT.md for cloud options
4. **Join community**: Open issues and discussions on GitHub

---

## Getting Help

- **Issues**: https://github.com/yourusername/traffic-violation-detection/issues
- **Discussions**: https://github.com/yourusername/traffic-violation-detection/discussions
- **Documentation**: README.md and inline code comments

**Enjoy using the Traffic Violation Detection System!** 🚀
