"""
Unit tests for helmet detection module
"""

import pytest
import numpy as np
import cv2
from backend.app.services.helmet_detection import HelmetDetector


class TestHelmetDetector:
    """Test cases for HelmetDetector"""
    
    @pytest.fixture
    def detector(self):
        """Create detector instance for testing"""
        # Use a mock model path
        return HelmetDetector(
            model_path="models/helmet_detection/best.pt",
            conf_threshold=0.5
        )
    
    def test_detector_initialization(self, detector):
        """Test detector initialization"""
        assert detector is not None
        assert detector.conf_threshold == 0.5
    
    def test_detect_violations(self):
        """Test violation detection logic"""
        from backend.app.services.helmet_detection import HelmetDetector
        
        # Create mock detections
        detections = {
            'helmets': [{'bbox': (10, 20, 100, 120), 'confidence': 0.95}],
            'no_helmets': [{'bbox': (150, 20, 250, 120), 'confidence': 0.87}]
        }
        
        violations = HelmetDetector.detect_violations(detector, detections)
        
        # Should find violations for no_helmet detections
        assert len(violations) == 1
        assert violations[0]['type'] == 'HELMET_NOT_WORN'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
