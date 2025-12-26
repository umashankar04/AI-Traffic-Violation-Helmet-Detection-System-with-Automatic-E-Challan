"""
Violation Detection Service
Core business logic for detecting violations
"""

import logging
from datetime import datetime
from typing import Dict, List, Tuple
from backend.app.models.database import (
    Violation, ViolationTypeEnum, ViolationSeverityEnum
)

logger = logging.getLogger(__name__)


class ViolationDetectionService:
    """
    Service for detecting and recording traffic violations
    """
    
    # Violation rules configuration
    VIOLATION_RULES = {
        ViolationTypeEnum.HELMET_NOT_WORN: {
            'penalty': 500,
            'severity': ViolationSeverityEnum.HIGH,
            'description': 'Rider not wearing helmet'
        },
        ViolationTypeEnum.TRIPLE_RIDING: {
            'penalty': 1000,
            'severity': ViolationSeverityEnum.HIGH,
            'description': 'More than 2 persons on 2-wheeler'
        },
        ViolationTypeEnum.SIGNAL_VIOLATION: {
            'penalty': 500,
            'severity': ViolationSeverityEnum.MEDIUM,
            'description': 'Traffic signal violation'
        },
        ViolationTypeEnum.SPEED_VIOLATION: {
            'penalty': 400,
            'severity': ViolationSeverityEnum.MEDIUM,
            'description': 'Speed limit exceeded'
        }
    }
    
    @staticmethod
    def create_violation(
        violation_type: ViolationTypeEnum,
        vehicle_number: str,
        latitude: float,
        longitude: float,
        location_name: str,
        image_path: str = None,
        detection_confidence: float = 0.0,
        vehicle_type: str = None
    ) -> Violation:
        """
        Create a violation record.
        
        Args:
            violation_type: Type of violation
            vehicle_number: Vehicle registration number
            latitude: Latitude of violation location
            longitude: Longitude of violation location
            location_name: Human-readable location name
            image_path: Path to evidence image
            detection_confidence: Model detection confidence
            vehicle_type: Type of vehicle
            
        Returns:
            Violation object
        """
        rule = ViolationDetectionService.VIOLATION_RULES.get(
            violation_type, 
            {'penalty': 0, 'severity': ViolationSeverityEnum.LOW, 'description': ''}
        )
        
        violation = Violation(
            violation_type=violation_type,
            severity=rule['severity'],
            description=rule['description'],
            vehicle_number=vehicle_number,
            vehicle_type=vehicle_type,
            latitude=latitude,
            longitude=longitude,
            location_name=location_name,
            image_path=image_path,
            detection_confidence=detection_confidence,
            timestamp=datetime.utcnow()
        )
        
        logger.info(f"Created violation: {violation_type} for vehicle {vehicle_number}")
        return violation
    
    @staticmethod
    def detect_helmet_violation(
        has_helmet: bool,
        vehicle_number: str,
        latitude: float,
        longitude: float,
        location_name: str,
        image_path: str = None,
        confidence: float = 0.0
    ) -> Violation:
        """
        Detect helmet violation specifically.
        
        Args:
            has_helmet: True if helmet detected, False otherwise
            vehicle_number: Vehicle number
            latitude: Location latitude
            longitude: Location longitude
            location_name: Location name
            image_path: Evidence image path
            confidence: Detection confidence
            
        Returns:
            Violation if helmet not worn, None otherwise
        """
        if not has_helmet:
            return ViolationDetectionService.create_violation(
                violation_type=ViolationTypeEnum.HELMET_NOT_WORN,
                vehicle_number=vehicle_number,
                latitude=latitude,
                longitude=longitude,
                location_name=location_name,
                image_path=image_path,
                detection_confidence=confidence,
                vehicle_type='Two-wheeler'
            )
        return None
    
    @staticmethod
    def get_violation_penalty(violation_type: ViolationTypeEnum) -> float:
        """Get penalty amount for violation type."""
        return ViolationDetectionService.VIOLATION_RULES.get(
            violation_type, {}
        ).get('penalty', 0)
    
    @staticmethod
    def get_violation_severity(violation_type: ViolationTypeEnum) -> ViolationSeverityEnum:
        """Get severity level for violation type."""
        return ViolationDetectionService.VIOLATION_RULES.get(
            violation_type, {}
        ).get('severity', ViolationSeverityEnum.LOW)


class ProcessingPipeline:
    """
    Processing pipeline for video/image streams
    """
    
    def __init__(self, helmet_detector, plate_ocr_pipeline):
        """
        Initialize processing pipeline.
        
        Args:
            helmet_detector: HelmetDetector service instance
            plate_ocr_pipeline: NumberPlateRecognitionPipeline instance
        """
        self.helmet_detector = helmet_detector
        self.plate_ocr_pipeline = plate_ocr_pipeline
        self.violations = []
    
    def process_frame(
        self,
        frame,
        latitude: float,
        longitude: float,
        location_name: str,
        save_evidence: bool = True
    ) -> Dict:
        """
        Process single frame for violations.
        
        Args:
            frame: Image frame (numpy array)
            latitude: Location latitude
            longitude: Location longitude
            location_name: Location name
            save_evidence: Whether to save evidence images
            
        Returns:
            Dictionary with violations and detections
        """
        results = {
            'violations': [],
            'helmet_detections': None,
            'plate_detections': None,
            'frame': frame
        }
        
        try:
            # Detect helmets
            helmet_detections = self.helmet_detector.detect(frame)
            results['helmet_detections'] = helmet_detections
            
            # Check for helmet violations
            helmet_violations = self.helmet_detector.detect_violations(helmet_detections)
            results['violations'].extend(helmet_violations)
            
            # Detect number plates
            plate_results = self.plate_ocr_pipeline.process_image(frame)
            results['plate_detections'] = plate_results
            
            # Associate violations with vehicle numbers
            for violation in results['violations']:
                if plate_results.get('valid_plates_found', 0) > 0:
                    for plate in plate_results['ocr'].get('valid_plates', []):
                        violation['vehicle_number'] = plate['text']
                        violation['latitude'] = latitude
                        violation['longitude'] = longitude
                        violation['location_name'] = location_name
            
            logger.info(f"Frame processed: {len(results['violations'])} violations detected")
            
        except Exception as e:
            logger.error(f"Error processing frame: {str(e)}")
        
        return results
