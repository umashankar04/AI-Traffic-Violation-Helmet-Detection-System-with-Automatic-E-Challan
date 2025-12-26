"""
Integration tests for complete pipeline
"""

import pytest
from backend.app.services.complete_pipeline import CompletePipeline


class TestCompletePipeline:
    """Test cases for end-to-end pipeline"""
    
    @pytest.fixture
    def pipeline(self):
        """Create pipeline instance"""
        return CompletePipeline(
            helmet_model_path="models/helmet_detection/best.pt",
            plate_model_path="models/plate_detection/best.pt",
            auto_issue_challan=False 
        )
    
    def test_pipeline_initialization(self, pipeline):
        """Test pipeline initialization"""
        assert pipeline is not None
        assert pipeline.helmet_detector is not None
        assert pipeline.plate_pipeline is not None
        assert pipeline.auto_issue_challan is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
