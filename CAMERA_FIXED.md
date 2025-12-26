# 🎥 Camera Troubleshooting Guide - RESOLVED

## ✅ Issue: Camera Not Opening

### Root Cause

OpenCV (cv2) requires **NumPy 1.x compatibility**, but Python 3.14 had NumPy 2.3.x installed, causing import errors.

### Solution Applied

1. **Downgraded NumPy** from 2.3.4 to 1.26.4
2. **Installed OpenCV 4.8.1** with pre-built wheels
3. **Verified camera works** with test script

### Status: ✅ **FIXED AND WORKING**

---

## 🚀 How to Start Using the System

### Step 1: API Server is Running

The API is now running on: **http://127.0.0.1:8001**

### Step 2: Open Web Interface

Visit: **http://127.0.0.1:8001/webcam**

### Step 3: Grant Camera Permission

- Browser will ask for camera permission (usually top-right notification)
- Click **"Allow"** to grant access to your webcam

### Step 4: Start Camera in Web Interface

- Click the **"START CAMERA"** button (green button with camera icon)
- Wait 1-2 seconds for the camera feed to appear
- You should see your webcam feed in the video stream area

### Step 5: Capture & Analyze

Once camera is running:

1. Click **"CAPTURE & ANALYZE"** button
2. System will capture photo and analyze for violations
3. Results display on the right panel:
   - **Violation Detected**: Yes/No
   - **Vehicle Number**: (from OCR)
   - **E-Challan Number**: (auto-generated if violation)
   - **Penalty Amount**: $50 (default)
   - **Timestamp**: When photo was captured

---

## 🔍 Camera Verification Results

Test script output shows:

- ✅ OpenCV version 4.8.1 working
- ✅ Camera device 0 opened successfully
- ✅ Frame capture working (720x1280, 3 channels)
- ✅ All 5 consecutive frame reads successful
- ✅ Camera properties set to 1280x720 @ 30 FPS

**Camera is fully functional!**

---

## ⚠️ If Camera Still Doesn't Show in Browser

### 1. **Browser Permissions**

- Go to browser settings → Privacy & security → Camera
- Make sure localhost:8001 is allowed
- Or add it to allowed list if not there

### 2. **Clear Browser Cache**

- Press **Ctrl+Shift+Delete** to open Clear Browsing Data
- Select **Cached images and files**
- Click **Clear data**
- Refresh the page

### 3. **Check Browser Console**

- Press **F12** to open Developer Tools
- Click **Console** tab
- Look for any error messages
- Common errors:
  - `Permission denied` → Grant camera access
  - `Camera not found` → Check camera is connected
  - `CORS error` → Restart browser and try again

### 4. **Try a Different Browser**

- Firefox, Chrome, Edge, Safari all support camera access
- Some work better than others for streaming

### 5. **Check Camera Device**

- Windows: Settings → Devices → Camera
- Ensure camera is listed and enabled
- Check if other apps are using it (Zoom, Teams, etc.)

### 6. **Restart Everything**

```
1. Close browser
2. Go to terminal running API (Ctrl+C to stop)
3. Unplug camera USB (wait 5 seconds)
4. Plug camera back in
5. Restart API: python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8001
6. Refresh browser: http://127.0.0.1:8001/webcam
7. Click "START CAMERA" button
```

---

## 📊 System Configuration

### Camera Settings

- **Device**: 0 (default/built-in webcam)
- **Resolution**: 1280x720 pixels
- **Frame Rate**: 30 FPS
- **Format**: BGR (OpenCV standard)

### API Server

- **Host**: 127.0.0.1 (localhost)
- **Port**: 8001
- **Framework**: FastAPI
- **Status**: ✅ Running and operational

### Database

- **Type**: PostgreSQL
- **Status**: Not connected (optional for demo)
- **Note**: System works without DB (data not persisted)

---

## 📡 Testing API Endpoints

If you want to test the API directly using cURL:

### Check API Health

```bash
curl http://127.0.0.1:8001/
```

### Start Camera

```bash
curl -X POST http://127.0.0.1:8001/api/camera/start
```

### Check Camera Status

```bash
curl http://127.0.0.1:8001/api/camera/status
```

### Get Current Frame (as Base64)

```bash
curl http://127.0.0.1:8001/api/camera/current-frame
```

### Capture & Analyze (with location)

```bash
curl -X POST http://127.0.0.1:8001/api/camera/capture \
  -F "latitude=28.7041" \
  -F "longitude=77.1025" \
  -F "location_name=Delhi"
```

### Stop Camera

```bash
curl -X POST http://127.0.0.1:8001/api/camera/stop
```

---

## 🔧 NumPy/OpenCV Compatibility Fixed

### What Was Wrong

- Python 3.14 comes with NumPy 2.3.x by default
- OpenCV 4.8.1 is compiled for NumPy 1.x
- This caused import errors: `AttributeError: _ARRAY_API not found`

### Solution

```bash
# Downgrade NumPy to 1.x
python -m pip install "numpy<2" --upgrade

# Install OpenCV (already working now)
python -m pip install opencv-python==4.8.1.78 --only-binary :all:
```

### Requirements Updated

If you reinstall, make sure to use:

```
numpy==1.26.4
opencv-python==4.8.1.78
```

---

## ✅ Next Steps

1. ✅ **Camera confirmed working** via test script
2. ✅ **API running** on port 8001
3. ✅ **Web interface accessible** at /webcam
4. **→ Next: Test capturing violations**
   - Start camera
   - Position webcam at a scene
   - Click "CAPTURE & ANALYZE"
   - View violation detection results

---

## 📞 Quick Reference

| Component       | Status       | URL                            |
| --------------- | ------------ | ------------------------------ |
| API Server      | ✅ Running   | http://127.0.0.1:8001          |
| Web Interface   | ✅ Ready     | http://127.0.0.1:8001/webcam   |
| Camera Hardware | ✅ Working   | Device 0                       |
| OpenCV          | ✅ 4.8.1     | Installed                      |
| NumPy           | ✅ 1.26.4    | Compatible                     |
| API Docs        | ✅ Available | http://127.0.0.1:8001/api/docs |

---

## 🎉 System is Ready!

Your camera-enabled traffic violation detection system is **fully operational**.

**Start capturing violations now:**

1. Open http://127.0.0.1:8001/webcam
2. Click "START CAMERA"
3. Click "CAPTURE & ANALYZE"
4. View instant E-Challan generation! 📸✅
