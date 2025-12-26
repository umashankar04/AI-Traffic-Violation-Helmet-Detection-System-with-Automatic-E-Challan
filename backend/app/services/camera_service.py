"""
Real-time camera capture and processing service
"""

from typing import Optional, Tuple, Dict, Any
import logging
import threading
from pathlib import Path
from datetime import datetime
import os

# Lazy imports for type hints
try:
    import numpy as np
except ImportError:
    np = None

logger = logging.getLogger(__name__)


class CameraCapture:
    """
    Real-time camera capture and processing
    """
    
    def __init__(self, camera_index: int = 0):
        """Initialize camera capture
        
        Args:
            camera_index: Camera device index (0 for default/built-in)
        """
        self.camera_index = camera_index
        self.cap = None
        self.is_running = False
        self.current_frame = None
        self.frame_count = 0
        self.lock = threading.Lock()
        
    def start(self) -> bool:
        """Start camera capture"""
        try:
            import cv2
            import numpy as np
            
            self.cap = cv2.VideoCapture(self.camera_index)
            if not self.cap.isOpened():
                logger.error(f"Failed to open camera {self.camera_index}")
                return False
            
            # Set camera properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            self.is_running = True
            
            # Start capture thread
            self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
            self.capture_thread.start()
            
            logger.info(f"Camera {self.camera_index} started successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error starting camera: {str(e)}")
            return False
    
    def _capture_loop(self):
        """Continuous capture loop"""
        import numpy as np
        
        while self.is_running:
            ret, frame = self.cap.read()
            if ret:
                with self.lock:
                    self.current_frame = frame
                    self.frame_count += 1
            else:
                logger.warning("Failed to read frame from camera")
    
    def get_frame(self) -> Optional["np.ndarray"]:
        """Get current frame"""
        with self.lock:
            return self.current_frame.copy() if self.current_frame is not None else None
    
    def capture_photo(self, output_dir: str = "data/evidence") -> Optional[str]:
        """Capture and save current frame
        
        Args:
            output_dir: Directory to save the photo
            
        Returns:
            Path to saved photo or None if failed
        """
        try:
            import cv2
            
            frame = self.get_frame()
            if frame is None:
                logger.error("No frame available to capture")
                return None
            
            # Create output directory if it doesn't exist
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = f"violation_{timestamp}.jpg"
            filepath = os.path.join(output_dir, filename)
            
            # Save image
            success = cv2.imwrite(filepath, frame)
            
            if success:
                logger.info(f"Photo captured: {filepath}")
                return filepath
            else:
                logger.error(f"Failed to write image to {filepath}")
                return None
                
        except Exception as e:
            logger.error(f"Error capturing photo: {str(e)}")
            return None
    
    def stop(self):
        """Stop camera capture"""
        try:
            self.is_running = False
            if self.capture_thread and self.capture_thread.is_alive():
                self.capture_thread.join(timeout=2)
            if self.cap:
                self.cap.release()
            logger.info("Camera stopped")
        except Exception as e:
            logger.error(f"Error stopping camera: {str(e)}")
    
    def __del__(self):
        """Cleanup on deletion"""
        self.stop()


class RealtimeDetectionPipeline:
    """
    Real-time detection pipeline for camera feed
    """
    
    def __init__(self):
        """Initialize pipeline"""
        self.helmet_detector = None
        self.plate_ocr = None
        self.violation_service = None
        self.echallan_service = None
        
    def initialize_services(self):
        """Initialize detection services"""
        try:
            # Try to load actual services, fall back to mock if not available
            try:
                from backend.app.services.helmet_detection import HelmetDetector
                self.helmet_detector = HelmetDetector()
                logger.info("Real helmet detector loaded")
            except Exception as e:
                logger.warning(f"Could not load helmet detector: {e}. Using mock detector.")
                self.helmet_detector = None
            
            try:
                from backend.app.services.plate_ocr import NumberPlateRecognitionPipeline
                self.plate_ocr = NumberPlateRecognitionPipeline()
                logger.info("Real plate OCR loaded")
            except Exception as e:
                logger.warning(f"Could not load plate OCR: {e}. Using mock OCR.")
                self.plate_ocr = None
            
            try:
                from backend.app.services.violation_detection import ViolationDetectionService
                self.violation_service = ViolationDetectionService()
            except:
                self.violation_service = None
            
            try:
                from backend.app.services.echallan import EChallanService
                self.echallan_service = EChallanService()
            except:
                self.echallan_service = None
            
            logger.info("Detection services initialized (using available services)")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing services: {str(e)}")
            return False
    
    def process_frame(
        self, 
        frame: "np.ndarray",
        latitude: float = 28.7041,
        longitude: float = 77.1025,
        location_name: str = "Delhi"
    ) -> Dict[str, Any]:
        """
        Process frame for violations and generate E-challan
        
        Args:
            frame: Image frame
            latitude: Location latitude
            longitude: Location longitude
            location_name: Location name
            
        Returns:
            Processing result with violations and challan
        """
        result = {
            "status": "processing",
            "violations_detected": 0,
            "vehicle_number": None,
            "helmet_violations": [],
            "plate_detections": [],
            "echallan_generated": False,
            "echallan_number": None,
            "penalty_amount": 0
        }
        
        try:
            import random
            import string
            
            # Detect helmets (or use mock detection)
            if self.helmet_detector:
                helmet_detections = self.helmet_detector.detect(frame)
                violations = self.helmet_detector.detect_violations(helmet_detections)
                result["helmet_violations"] = len(violations)
                result["violations_detected"] += len(violations)
            else:
                # Mock detection: randomly detect violation for demo
                result["helmet_violations"] = 1
                result["violations_detected"] = 1
                logger.info("Using mock helmet detection - violation detected")
            
            # Detect number plate (or use mock)
            if self.plate_ocr:
                plate_results = self.plate_ocr.process_image(frame)
                if plate_results and plate_results.get("plates"):
                    result["vehicle_number"] = plate_results["plates"][0] if plate_results["plates"] else None
                    result["plate_detections"] = plate_results["plates"]
            else:
                # Mock plate detection: generate random plate for demo
                mock_plate = f"DL{random.randint(1,20)}C{random.randint(1000,9999)}"
                result["vehicle_number"] = mock_plate
                result["plate_detections"] = [mock_plate]
                logger.info(f"Using mock plate OCR - plate: {mock_plate}")
            
            # Generate E-challan if violation detected
            if result["violations_detected"] > 0 and result["vehicle_number"]:
                try:
                    # Create violation record (would save to DB in production)
                    violation_data = {
                        "vehicle_number": result["vehicle_number"],
                        "violation_type": "HELMET_NOT_WORN",
                        "severity": "HIGH",
                        "latitude": latitude,
                        "longitude": longitude,
                        "location_name": location_name,
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    # Generate E-challan number
                    if self.echallan_service:
                        challan_number = self.echallan_service.generate_challan_number()
                    else:
                        # Mock challan number
                        date_str = datetime.now().strftime("%Y%m%d")
                        random_num = ''.join(random.choices(string.digits, k=5))
                        challan_number = f"ECH-{date_str}-{random_num}"
                    
                    penalty = 500  # Default helmet violation penalty (₹500 or $50)
                    
                    result["echallan_generated"] = True
                    result["echallan_number"] = challan_number
                    result["penalty_amount"] = penalty
                    
                    logger.info(f"E-challan generated: {challan_number} for {result['vehicle_number']} - Penalty: ₹{penalty}")
                    
                except Exception as e:
                    logger.error(f"Error generating E-challan: {str(e)}")
                    result["echallan_generated"] = False
            
            result["status"] = "success"
            
        except Exception as e:
            logger.error(f"Error processing frame: {str(e)}")
            result["status"] = "error"
            result["error"] = str(e)
        
        return result


# Global camera instance
_camera_instance: Optional[CameraCapture] = None


def get_camera() -> CameraCapture:
    """Get or create camera instance"""
    global _camera_instance
    if _camera_instance is None:
        _camera_instance = CameraCapture(camera_index=0)
    return _camera_instance


def start_camera() -> bool:
    """Start global camera"""
    camera = get_camera()
    return camera.start()


def stop_camera():
    """Stop global camera"""
    global _camera_instance
    if _camera_instance:
        _camera_instance.stop()
        _camera_instance = None
