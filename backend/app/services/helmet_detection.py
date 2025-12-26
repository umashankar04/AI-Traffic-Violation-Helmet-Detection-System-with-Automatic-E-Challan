"""
Helmet Detection Inference Module
Real-time helmet detection from video/image streams
"""

import logging
import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO
import torch

logger = logging.getLogger(__name__)


class HelmetDetector:
    """
    Real-time helmet detection from video/image streams using YOLOv8
    """
    
    def __init__(self, model_path: str, conf_threshold: float = 0.5, device: str = None):
        """
        Initialize helmet detector.
        
        Args:
            model_path: Path to trained YOLO model
            conf_threshold: Confidence threshold for detections
            device: Device to run model on ('cuda' or 'cpu')
        """
        self.conf_threshold = conf_threshold
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        
        logger.info(f"Loading helmet detection model from {model_path}")
        self.model = YOLO(model_path)
        self.model.to(self.device)
        
        # Class mapping
        self.class_names = {0: "helmet", 1: "no_helmet"}
        self.class_colors = {0: (0, 255, 0), 1: (0, 0, 255)}  # Green for helmet, Red for no_helmet
    
    def detect(self, image: np.ndarray, return_crops: bool = False) -> dict:
        """
        Detect helmets in image.
        
        Args:
            image: Input image (BGR format)
            return_crops: If True, return cropped regions
            
        Returns:
            Dictionary containing detections and metadata
        """
        results = self.model.predict(source=image, conf=self.conf_threshold, verbose=False)
        
        detections = {
            'helmets': [],
            'no_helmets': [],
            'frame': image.copy(),
            'raw_results': results
        }
        
        for result in results:
            if result.boxes is not None:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = float(box.conf[0])
                    class_id = int(box.cls[0])
                    class_name = self.class_names[class_id]
                    
                    detection = {
                        'bbox': (x1, y1, x2, y2),
                        'confidence': conf,
                        'class_id': class_id,
                        'class_name': class_name,
                        'area': (x2 - x1) * (y2 - y1)
                    }
                    
                    if return_crops:
                        detection['crop'] = image[y1:y2, x1:x2].copy()
                    
                    if class_id == 0:
                        detections['helmets'].append(detection)
                    else:
                        detections['no_helmets'].append(detection)
        
        return detections
    
    def detect_violations(self, detections: dict) -> list:
        """
        Identify helmet violations.
        Violation = Person detected with no helmet
        
        Args:
            detections: Detection results from detect()
            
        Returns:
            List of violations found
        """
        violations = []
        
        # Simple rule: if no_helmet detections exist, it's a violation
        for no_helmet in detections['no_helmets']:
            violation = {
                'type': 'HELMET_NOT_WORN',
                'bbox': no_helmet['bbox'],
                'confidence': no_helmet['confidence'],
                'severity': 'HIGH',
                'penalty': 500  # INR
            }
            violations.append(violation)
        
        return violations
    
    def draw_detections(self, image: np.ndarray, detections: dict, 
                       draw_violations: bool = True) -> np.ndarray:
        """
        Draw detection boxes on image.
        
        Args:
            image: Input image
            detections: Detection results
            draw_violations: If True, highlight violations in red
            
        Returns:
            Image with drawn detections
        """
        output = image.copy()
        
        # Draw helmet detections (green)
        for detection in detections['helmets']:
            x1, y1, x2, y2 = detection['bbox']
            conf = detection['confidence']
            cv2.rectangle(output, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(output, f"Helmet {conf:.2f}", (x1, y1 - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Draw no-helmet detections (red)
        for detection in detections['no_helmets']:
            x1, y1, x2, y2 = detection['bbox']
            conf = detection['confidence']
            cv2.rectangle(output, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(output, f"No Helmet {conf:.2f}", (x1, y1 - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        return output
    
    def process_video(self, video_path: str, output_path: str = None, 
                     frame_skip: int = 5) -> dict:
        """
        Process video file and detect helmets.
        
        Args:
            video_path: Path to input video
            output_path: Path to save output video (optional)
            frame_skip: Process every nth frame
            
        Returns:
            Dictionary with statistics
        """
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        writer = None
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        stats = {
            'total_frames': 0,
            'processed_frames': 0,
            'total_detections': 0,
            'violations': 0,
            'helmets_found': 0,
            'no_helmets_found': 0
        }
        
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            stats['total_frames'] += 1
            
            # Process every nth frame
            if frame_count % frame_skip == 0:
                stats['processed_frames'] += 1
                
                # Detect helmets
                detections = self.detect(frame)
                stats['helmets_found'] += len(detections['helmets'])
                stats['no_helmets_found'] += len(detections['no_helmets'])
                stats['total_detections'] += len(detections['helmets']) + len(detections['no_helmets'])
                
                # Check violations
                violations = self.detect_violations(detections)
                stats['violations'] += len(violations)
                
                # Draw on frame
                frame = self.draw_detections(frame, detections)
            
            if writer:
                writer.write(frame)
            
            frame_count += 1
        
        cap.release()
        if writer:
            writer.release()
        
        logger.info(f"Video processing completed: {stats}")
        return stats


if __name__ == "__main__":
    # Example usage
    detector = HelmetDetector("models/helmet_detection/best.pt")
    
    # Process image
    image = cv2.imread("test_image.jpg")
    detections = detector.detect(image)
    violations = detector.detect_violations(detections)
    
    output = detector.draw_detections(image, detections)
    cv2.imwrite("output.jpg", output)
    
    print(f"Found {len(detections['helmets'])} helmets and {len(detections['no_helmets'])} no-helmets")
    print(f"Violations: {len(violations)}")
