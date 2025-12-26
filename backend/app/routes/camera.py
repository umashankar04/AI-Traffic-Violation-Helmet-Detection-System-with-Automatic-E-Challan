"""
Real-time camera and photo capture API endpoints
"""

from fastapi import APIRouter, HTTPException, Form
from fastapi.responses import StreamingResponse, JSONResponse
import logging
from typing import Optional
import base64
from datetime import datetime

router = APIRouter(prefix="/api/camera", tags=["camera"])
logger = logging.getLogger(__name__)


@router.post("/start")
async def start_camera():
    """Start real-time camera capture"""
    try:
        from backend.app.services.camera_service import start_camera
        
        success = start_camera()
        if success:
            return {
                "status": "success",
                "message": "Camera started successfully",
                "stream_url": "/api/camera/stream"
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to start camera")
            
    except Exception as e:
        logger.error(f"Error starting camera: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stop")
async def stop_camera():
    """Stop camera capture"""
    try:
        from backend.app.services.camera_service import stop_camera
        
        stop_camera()
        return {
            "status": "success",
            "message": "Camera stopped successfully"
        }
        
    except Exception as e:
        logger.error(f"Error stopping camera: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stream")
async def camera_stream():
    """Stream real-time camera feed (MJPEG)"""
    try:
        import cv2
        from backend.app.services.camera_service import get_camera
        
        camera = get_camera()
        
        def generate_stream():
            """Generate MJPEG stream"""
            while True:
                frame = camera.get_frame()
                if frame is None:
                    continue
                
                # Encode frame to JPEG
                ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                if not ret:
                    continue
                
                # Yield frame in MJPEG format
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n'
                       b'Content-Length: ' + str(len(buffer)).encode() + b'\r\n\r\n'
                       + buffer.tobytes() + b'\r\n')
        
        return StreamingResponse(
            generate_stream(),
            media_type="multipart/x-mixed-replace; boundary=frame"
        )
        
    except Exception as e:
        logger.error(f"Error streaming camera: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/capture")
async def capture_photo(
    latitude: float = Form(default=28.7041),
    longitude: float = Form(default=77.1025),
    location_name: str = Form(default="Delhi")
):
    """
    Capture photo and generate E-challan if violation detected
    
    Args:
        latitude: Location latitude
        longitude: Location longitude
        location_name: Location name
        
    Returns:
        Photo with violation and E-challan info
    """
    try:
        from backend.app.services.camera_service import get_camera, RealtimeDetectionPipeline
        import numpy as np
        
        camera = get_camera()
        frame = camera.get_frame()
        
        if frame is None:
            raise HTTPException(status_code=400, detail="No camera frame available")
        
        # Save photo
        photo_path = camera.capture_photo()
        if not photo_path:
            raise HTTPException(status_code=500, detail="Failed to capture photo")
        
        # Process for violations
        pipeline = RealtimeDetectionPipeline()
        pipeline.initialize_services()
        
        result = pipeline.process_frame(
            frame,
            latitude=latitude,
            longitude=longitude,
            location_name=location_name
        )
        
        # Add photo path to result
        result["photo_path"] = photo_path
        result["timestamp"] = datetime.now().isoformat()
        
        return {
            "status": result["status"],
            "photo": photo_path,
            "violations_detected": result["violations_detected"],
            "vehicle_number": result["vehicle_number"],
            "helmet_violation_count": result["helmet_violations"],
            "echallan_generated": result["echallan_generated"],
            "echallan_number": result["echallan_number"],
            "penalty_amount": result["penalty_amount"],
            "timestamp": result["timestamp"],
            "location": {
                "latitude": latitude,
                "longitude": longitude,
                "name": location_name
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error capturing photo: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/current-frame")
async def get_current_frame():
    """Get current frame as base64-encoded image"""
    try:
        import cv2
        from backend.app.services.camera_service import get_camera
        import base64
        
        camera = get_camera()
        frame = camera.get_frame()
        
        if frame is None:
            raise HTTPException(status_code=400, detail="No frame available")
        
        # Encode to JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            raise HTTPException(status_code=500, detail="Failed to encode frame")
        
        # Convert to base64
        img_base64 = base64.b64encode(buffer).decode()
        
        return {
            "status": "success",
            "image": img_base64,
            "format": "jpeg",
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting frame: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/detect-violation")
async def detect_violation_realtime(
    latitude: float = Form(default=28.7041),
    longitude: float = Form(default=77.1025),
    location_name: str = Form(default="Delhi")
):
    """
    Analyze current frame for violations without capturing
    
    Returns:
        Violation detection results
    """
    try:
        from backend.app.services.camera_service import get_camera, RealtimeDetectionPipeline
        
        camera = get_camera()
        frame = camera.get_frame()
        
        if frame is None:
            raise HTTPException(status_code=400, detail="No camera frame available")
        
        # Process frame
        pipeline = RealtimeDetectionPipeline()
        pipeline.initialize_services()
        
        result = pipeline.process_frame(
            frame,
            latitude=latitude,
            longitude=longitude,
            location_name=location_name
        )
        
        return {
            "status": result["status"],
            "violations_detected": result["violations_detected"],
            "vehicle_number": result["vehicle_number"],
            "helmet_violations": result["helmet_violations"],
            "echallan_generated": result["echallan_generated"],
            "echallan_number": result["echallan_number"],
            "penalty_amount": result["penalty_amount"],
            "timestamp": datetime.now().isoformat(),
            "location": {
                "latitude": latitude,
                "longitude": longitude,
                "name": location_name
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error detecting violation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def camera_status():
    """Get camera status"""
    try:
        from backend.app.services.camera_service import get_camera
        
        camera = get_camera()
        frame = camera.get_frame()
        
        return {
            "status": "running" if camera.is_running and frame is not None else "stopped",
            "camera_index": camera.camera_index,
            "frames_captured": camera.frame_count,
            "has_frame": frame is not None
        }
        
    except Exception as e:
        logger.error(f"Error getting camera status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
