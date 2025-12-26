"""
Training script for Number Plate Detection Model (YOLOv8)
"""

import logging
import argparse
import yaml
from pathlib import Path
import torch
from ultralytics import YOLO
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class PlateDetectionTrainer:
    """
    Trainer for YOLOv8 number plate detection model
    """
    
    def __init__(self, config_path: str = None):
        """Initialize trainer."""
        self.config_path = config_path or "config/config.yaml"
        self.load_config()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")
    
    def load_config(self):
        """Load configuration."""
        with open(self.config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        logger.info(f"Configuration loaded from {self.config_path}")
    
    def prepare_dataset(self, data_dir: str, train_split: float = 0.8):
        """
        Prepare dataset in YOLO format.
        Expected: data/number_plate/images/ and data/number_plate/labels/
        """
        logger.info(f"Preparing dataset from {data_dir}")
        
        data_root = Path(data_dir)
        yolo_dir = data_root / "yolo_format"
        
        # Create YOLO directory structure
        for split in ["train", "val"]:
            (yolo_dir / split / "images").mkdir(parents=True, exist_ok=True)
            (yolo_dir / split / "labels").mkdir(parents=True, exist_ok=True)
        
        # Create dataset.yaml
        dataset_yaml = {
            'path': str(yolo_dir),
            'train': 'train/images',
            'val': 'val/images',
            'nc': 1,
            'names': {0: 'number_plate'}
        }
        
        dataset_yaml_path = yolo_dir / "dataset.yaml"
        with open(dataset_yaml_path, 'w') as f:
            yaml.dump(dataset_yaml, f)
        
        logger.info(f"Dataset YAML saved to {dataset_yaml_path}")
        return str(dataset_yaml_path)
    
    def train(self, dataset_yaml: str, epochs: int = 80, batch_size: int = 16, 
              img_size: int = 640):
        """Train YOLO plate detection model."""
        logger.info("Starting YOLOv8 Plate Detection Training")
        
        model = YOLO("yolov8m.pt")
        
        results = model.train(
            data=dataset_yaml,
            epochs=epochs,
            imgsz=img_size,
            batch=batch_size,
            device=self.device,
            project="models/plate_detection",
            name="plate_detector",
            save=True,
            half=True if self.device == "cuda" else False,
            patience=15
        )
        
        logger.info("Training completed")
        return model, results


def main():
    parser = argparse.ArgumentParser(description="Train YOLOv8 Plate Detection Model")
    parser.add_argument("--data", type=str, default="data/number_plate", 
                       help="Path to plate dataset")
    parser.add_argument("--epochs", type=int, default=80, help="Number of epochs")
    parser.add_argument("--batch-size", type=int, default=16, help="Batch size")
    parser.add_argument("--img-size", type=int, default=640, help="Image size")
    
    args = parser.parse_args()
    
    trainer = PlateDetectionTrainer()
    dataset_yaml = trainer.prepare_dataset(args.data)
    model, results = trainer.train(
        dataset_yaml=dataset_yaml,
        epochs=args.epochs,
        batch_size=args.batch_size,
        img_size=args.img_size
    )
    
    logger.info("Plate detection training completed!")


if __name__ == "__main__":
    main()
