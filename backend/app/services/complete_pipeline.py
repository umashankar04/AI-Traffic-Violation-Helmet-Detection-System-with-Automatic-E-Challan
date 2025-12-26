"""
Complete End-to-End Violation Processing Pipeline
"""

import logging
import cv2
from pathlib import Path
from backend.app.services.helmet_detection import HelmetDetector
from backend.app.services.plate_ocr import NumberPlateRecognitionPipeline
from backend.app.services.violation_detection import ProcessingPipeline, ViolationDetectionService
from backend.app.services.echallan import EChallanService
from sqlalchemy.orm import Session
from backend.app.database.database import SessionLocal
from backend.app.models.database import Violation, Challan

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class CompletePipeline:
    """
    Complete pipeline: Detection → Violation Rules → E-Challan
    """
    
    def __init__(
        self,
        helmet_model_path: str,
        plate_model_path: str,
        auto_issue_challan: bool = False
    ):
        """
        Initialize complete pipeline.
        
        Args:
            helmet_model_path: Path to helmet detection model
            plate_model_path: Path to plate detection model
            auto_issue_challan: Automatically issue E-challan
        """
        self.helmet_detector = HelmetDetector(helmet_model_path)
        self.plate_pipeline = NumberPlateRecognitionPipeline(
            plate_detector_model=plate_model_path
        )
        self.processing_pipeline = ProcessingPipeline(
            helmet_detector=self.helmet_detector,
            plate_ocr_pipeline=self.plate_pipeline
        )
        self.auto_issue_challan = auto_issue_challan
        self.db = SessionLocal()
    
    def process_image(
        self,
        image_path: str,
        latitude: float,
        longitude: float,
        location_name: str,
        save_evidence: bool = True
    ):
        """
        Process single image for complete violation detection and E-challan.
        
        Args:
            image_path: Path to image
            latitude: Location latitude
            longitude: Location longitude
            location_name: Location name
            save_evidence: Save evidence images
            
        Returns:
            Violations and challans generated
        """
        logger.info(f"Processing image: {image_path}")
        
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            logger.error(f"Failed to read image: {image_path}")
            return None
        
        # Process frame
        results = self.processing_pipeline.process_frame(
            frame=image,
            latitude=latitude,
            longitude=longitude,
            location_name=location_name,
            save_evidence=save_evidence
        )
        
        # Store violations in database
        violations = []
        for violation_data in results['violations']:
            violation = ViolationDetectionService.create_violation(
                violation_type=violation_data.get('type'),
                vehicle_number=violation_data.get('vehicle_number', 'UNKNOWN'),
                latitude=latitude,
                longitude=longitude,
                location_name=location_name,
                image_path=image_path if save_evidence else None,
                detection_confidence=violation_data.get('confidence', 0.0)
            )
            self.db.add(violation)
            self.db.commit()
            violations.append(violation)
            logger.info(f"Created violation: {violation.id}")
            
            # Auto-issue E-challan if enabled
            if self.auto_issue_challan:
                challan = EChallanService.create_challan(
                    violation_id=violation.id,
                    violation=violation,
                    evidence_image_url=image_path
                )
                self.db.add(challan)
                self.db.commit()
                logger.info(f"Auto-issued challan: {challan.challan_number}")
        
        return {
            'violations_found': len(violations),
            'violations': violations,
            'detections': results
        }
    
    def process_video(
        self,
        video_path: str,
        latitude: float,
        longitude: float,
        location_name: str,
        output_path: str = None,
        frame_skip: int = 5
    ):
        """
        Process video file for violations.
        
        Args:
            video_path: Path to video file
            latitude: Location latitude
            longitude: Location longitude
            location_name: Location name
            output_path: Output video path with annotations
            frame_skip: Process every nth frame
            
        Returns:
            Statistics
        """
        logger.info(f"Processing video: {video_path}")
        
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
            'total_violations': 0,
            'unique_vehicles': set(),
            'challans_issued': 0
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
                
                # Process frame
                results = self.processing_pipeline.process_frame(
                    frame=frame,
                    latitude=latitude,
                    longitude=longitude,
                    location_name=location_name
                )
                
                # Count violations
                stats['total_violations'] += len(results['violations'])
                
                # Store in database
                for violation_data in results['violations']:
                    vehicle_num = violation_data.get('vehicle_number', 'UNKNOWN')
                    stats['unique_vehicles'].add(vehicle_num)
                    
                    violation = ViolationDetectionService.create_violation(
                        violation_type=violation_data.get('type'),
                        vehicle_number=vehicle_num,
                        latitude=latitude,
                        longitude=longitude,
                        location_name=location_name,
                        detection_confidence=violation_data.get('confidence', 0.0)
                    )
                    self.db.add(violation)
                    
                    if self.auto_issue_challan:
                        challan = EChallanService.create_challan(
                            violation_id=violation.id,
                            violation=violation
                        )
                        self.db.add(challan)
                        stats['challans_issued'] += 1
                
                self.db.commit()
                
                # Draw on frame
                if results['helmet_detections']:
                    frame = self.helmet_detector.draw_detections(
                        frame, results['helmet_detections']
                    )
            
            if writer:
                writer.write(frame)
            
            frame_count += 1
        
        cap.release()
        if writer:
            writer.release()
        
        stats['unique_vehicles'] = len(stats['unique_vehicles'])
        logger.info(f"Video processing completed: {stats}")
        return stats
    
    def process_rtsp_stream(
        self,
        rtsp_url: str,
        latitude: float,
        longitude: float,
        location_name: str,
        duration_seconds: int = 300
    ):
        """
        Process live RTSP stream.
        
        Args:
            rtsp_url: RTSP stream URL
            latitude: Location latitude
            longitude: Location longitude
            location_name: Location name
            duration_seconds: How long to process
            
        Returns:
            Statistics
        """
        logger.info(f"Connecting to RTSP stream: {rtsp_url}")
        
        cap = cv2.VideoCapture(rtsp_url)
        if not cap.isOpened():
            logger.error(f"Failed to open RTSP stream: {rtsp_url}")
            return None
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(fps * duration_seconds)
        
        stats = {
            'stream_url': rtsp_url,
            'duration': duration_seconds,
            'total_frames_processed': 0,
            'total_violations': 0,
            'challans_issued': 0
        }
        
        import time
        start_time = time.time()
        
        frame_count = 0
        while (time.time() - start_time) < duration_seconds:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process every 5th frame for real-time performance
            if frame_count % 5 == 0:
                stats['total_frames_processed'] += 1
                
                results = self.processing_pipeline.process_frame(
                    frame=frame,
                    latitude=latitude,
                    longitude=longitude,
                    location_name=location_name
                )
                
                stats['total_violations'] += len(results['violations'])
                
                if self.auto_issue_challan:
                    stats['challans_issued'] += len(results['violations'])
            
            frame_count += 1
        
        cap.release()
        logger.info(f"RTSP stream processing completed: {stats}")
        return stats


def main():
    """Example usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="End-to-end violation processing")
    parser.add_argument("--image", type=str, help="Image file path")
    parser.add_argument("--video", type=str, help="Video file path")
    parser.add_argument("--latitude", type=float, required=True, help="Location latitude")
    parser.add_argument("--longitude", type=float, required=True, help="Location longitude")
    parser.add_argument("--location", type=str, required=True, help="Location name")
    parser.add_argument("--output", type=str, help="Output video path")
    parser.add_argument("--auto-challan", action="store_true", help="Auto-issue E-challans")
    
    args = parser.parse_args()
    
    # Initialize pipeline
    pipeline = CompletePipeline(
        helmet_model_path="models/helmet_detection/best.pt",
        plate_model_path="models/plate_detection/best.pt",
        auto_issue_challan=args.auto_challan
    )
    
    # Process based on input type
    if args.image:
        results = pipeline.process_image(
            image_path=args.image,
            latitude=args.latitude,
            longitude=args.longitude,
            location_name=args.location
        )
        logger.info(f"Results: {results}")
    
    elif args.video:
        stats = pipeline.process_video(
            video_path=args.video,
            latitude=args.latitude,
            longitude=args.longitude,
            location_name=args.location,
            output_path=args.output
        )
        logger.info(f"Video processing stats: {stats}")


if __name__ == "__main__":
    main()
