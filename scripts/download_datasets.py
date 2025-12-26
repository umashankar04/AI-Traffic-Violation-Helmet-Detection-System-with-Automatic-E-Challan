"""
Training Data Downloader Script
Downloads and prepares datasets for helmet and plate detection
"""

import os
import logging
from pathlib import Path
import urllib.request
import json

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class DatasetDownloader:
    """
    Download and prepare datasets for training
    """
    
    HELMET_DATASETS = {
        "helmet-detection-kaggle": {
            "url": "https://www.kaggle.com/datasets/andrewmvd/helmet-detection",
            "description": "Helmet detection dataset from Kaggle",
            "source": "Kaggle",
            "download_instructions": """
            1. Visit: https://www.kaggle.com/datasets/andrewmvd/helmet-detection
            2. Click 'Download' button
            3. Extract to data/helmet/images/
            4. Run: python scripts/prepare_helmet_dataset.py
            """
        },
        "roboflow-helmet": {
            "url": "https://universe.roboflow.com/",
            "description": "Helmet detection from Roboflow",
            "source": "Roboflow",
            "download_instructions": """
            1. Visit: https://universe.roboflow.com/
            2. Search for 'helmet detection'
            3. Select dataset and download
            4. Extract to data/helmet/
            """
        }
    }
    
    PLATE_DATASETS = {
        "indian-vehicle-plate-kaggle": {
            "url": "https://www.kaggle.com/datasets",
            "description": "Indian vehicle number plate dataset",
            "source": "Kaggle",
            "download_instructions": """
            1. Search Kaggle for 'Indian vehicle number plate'
            2. Download and extract to data/number_plate/
            """
        },
        "open-images-plates": {
            "url": "https://github.com/openimages/dataset",
            "description": "Open Images dataset - number plates",
            "source": "Google Open Images",
            "download_instructions": """
            1. Use Open Images downloader
            2. Filter for license plates/vehicle registration
            3. Extract to data/number_plate/
            """
        }
    }
    
    @staticmethod
    def print_download_guide():
        """Print guide for downloading datasets."""
        print("\n" + "="*80)
        print("DATASET DOWNLOAD GUIDE".center(80))
        print("="*80)
        
        print("\n📌 HELMET DETECTION DATASETS:\n")
        for dataset_name, details in DatasetDownloader.HELMET_DATASETS.items():
            print(f"🔹 {dataset_name.upper()}")
            print(f"   Source: {details['source']}")
            print(f"   Description: {details['description']}")
            print(f"   Instructions:\n{details['download_instructions']}")
            print()
        
        print("\n📌 NUMBER PLATE DATASETS:\n")
        for dataset_name, details in DatasetDownloader.PLATE_DATASETS.items():
            print(f"🔹 {dataset_name.upper()}")
            print(f"   Source: {details['source']}")
            print(f"   Description: {details['description']}")
            print(f"   Instructions:\n{details['download_instructions']}")
            print()
        
        print("="*80)
        print("\n⚠️  IMPORTANT NOTES:")
        print("   • Most datasets require manual Kaggle account & API key")
        print("   • Respect dataset licenses and usage terms")
        print("   • Some datasets are large (1-5 GB)")
        print("   • You can also collect custom data from local traffic cameras")
        print("="*80 + "\n")
    
    @staticmethod
    def prepare_dataset_structure():
        """Create required directory structure."""
        dirs = [
            "data/helmet/images/helmet",
            "data/helmet/images/no_helmet",
            "data/helmet/labels",
            "data/helmet/yolo_format/train/images",
            "data/helmet/yolo_format/train/labels",
            "data/helmet/yolo_format/val/images",
            "data/helmet/yolo_format/val/labels",
            "data/number_plate/images",
            "data/number_plate/labels",
            "data/number_plate/yolo_format/train/images",
            "data/number_plate/yolo_format/train/labels",
            "data/number_plate/yolo_format/val/images",
            "data/number_plate/yolo_format/val/labels",
        ]
        
        for directory in dirs:
            Path(directory).mkdir(parents=True, exist_ok=True)
            logger.info(f"✓ Created directory: {directory}")
    
    @staticmethod
    def download_yolov8_models():
        """Download pre-trained YOLOv8 models."""
        try:
            from ultralytics import YOLO
            
            logger.info("Downloading YOLOv8 models...")
            
            # Medium models (good balance between speed and accuracy)
            models = ["yolov8m.pt", "yolov8m-seg.pt"]
            
            for model in models:
                try:
                    logger.info(f"Downloading {model}...")
                    YOLO(model)  # This automatically downloads if not present
                    logger.info(f"✓ {model} downloaded successfully")
                except Exception as e:
                    logger.error(f"✗ Failed to download {model}: {str(e)}")
        
        except ImportError:
            logger.error("ultralytics not installed. Install with: pip install ultralytics")


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Download and prepare datasets for model training"
    )
    parser.add_argument(
        "--guide",
        action="store_true",
        help="Print dataset download guide"
    )
    parser.add_argument(
        "--prepare",
        action="store_true",
        help="Prepare directory structure"
    )
    parser.add_argument(
        "--download-models",
        action="store_true",
        help="Download pre-trained YOLOv8 models"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all preparation steps"
    )
    
    args = parser.parse_args()
    
    if args.guide or args.all:
        DatasetDownloader.print_download_guide()
    
    if args.prepare or args.all:
        logger.info("Preparing dataset structure...")
        DatasetDownloader.prepare_dataset_structure()
    
    if args.download_models or args.all:
        logger.info("Downloading models...")
        DatasetDownloader.download_yolov8_models()
    
    if not (args.guide or args.prepare or args.download_models or args.all):
        parser.print_help()


if __name__ == "__main__":
    main()
