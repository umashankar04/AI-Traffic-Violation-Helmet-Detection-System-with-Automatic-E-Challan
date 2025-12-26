"""
Simple camera test script to diagnose camera issues
"""

import cv2
import sys

print("=" * 60)
print("Camera Diagnostic Test")
print("=" * 60)

# Test 1: Check OpenCV version
print(f"\n✓ OpenCV version: {cv2.__version__}")

# Test 2: Try to open camera
print("\n[Test 1] Attempting to open camera device 0...")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("✗ FAILED: Could not open camera device 0")
    print("\nPossible causes:")
    print("  1. No camera connected to computer")
    print("  2. Camera is being used by another application")
    print("  3. Camera permissions not granted")
    print("  4. Camera drivers not installed or outdated")
    print("\nSolutions:")
    print("  - Check Device Manager for camera device")
    print("  - Close other apps using camera (Zoom, Teams, etc.)")
    print("  - Check camera permissions in Windows Settings")
    print("  - Update camera drivers")
    sys.exit(1)

print("✓ Camera device 0 opened successfully")

# Test 3: Try to read frames
print("\n[Test 2] Attempting to read frames from camera...")
try:
    ret, frame = cap.read()
    if ret:
        print(f"✓ Successfully read frame")
        print(f"  Frame shape: {frame.shape}")
        print(f"  Frame size: {frame.size} bytes")
    else:
        print("✗ FAILED: Could not read frame from camera")
        print("  Try reconnecting the camera and try again")
        cap.release()
        sys.exit(1)
except Exception as e:
    print(f"✗ ERROR reading frame: {e}")
    cap.release()
    sys.exit(1)

# Test 4: Set camera properties
print("\n[Test 3] Setting camera properties...")
try:
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    print(f"✓ Camera properties set:")
    print(f"  Resolution: {width}x{height}")
    print(f"  FPS: {fps}")
except Exception as e:
    print(f"✗ ERROR setting properties: {e}")

# Test 5: Read multiple frames
print("\n[Test 4] Reading 5 consecutive frames...")
try:
    for i in range(5):
        ret, frame = cap.read()
        if ret:
            print(f"  ✓ Frame {i+1}: OK (shape: {frame.shape})")
        else:
            print(f"  ✗ Frame {i+1}: FAILED")
            break
except Exception as e:
    print(f"✗ ERROR reading frames: {e}")

# Cleanup
cap.release()

print("\n" + "=" * 60)
print("✓ All camera tests passed!")
print("=" * 60)
print("\nCamera is working properly.")
print("If you still have issues with the web interface:")
print("  1. Clear browser cache and refresh")
print("  2. Check browser console for JavaScript errors (F12)")
print("  3. Make sure to click 'START CAMERA' in web interface")
print("  4. Wait 2-3 seconds for camera to initialize")
