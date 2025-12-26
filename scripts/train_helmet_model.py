"""
Phase 1: Helmet Detection Model - Training Pipeline
YOLOv8 model for binary classification: Helmet / No Helmet
"""

import os
import yaml
import logging
import argparse
from pathlib import Path
import numpy as np
import torch
from ultralytics import YOLO
from sklearn.model_selection import train_test_split
import cv2

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HelmetDetectionTrainer:
    """
    Trainer class for YOLOv8 helmet detection model.
    Handles dataset preparation, model training, and evaluation.
    """
    
    def __init__(self, config_path: str = None):
        """Initialize trainer with configuration."""
        self.config_path = config_path or "config/config.yaml"
        self.load_config()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")
    
    def load_config(self):
        """Load configuration from YAML file."""
        with open(self.config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        logger.info(f"Configuration loaded from {self.config_path}")
    
    def prepare_dataset(self, data_dir: str, train_split: float = 0.8):
        """
        Prepare dataset in YOLO format.
        Expected directory structure:
        data/helmet/
        ├── helmet/
        └── no_helmet/
        """
        logger.info(f"Preparing dataset from {data_dir}")
        
        data_root = Path(data_dir)
        yolo_dir = data_root / "yolo_format"
        
        # Create YOLO directory structure
        for split in ["train", "val"]:
            (yolo_dir / split / "images").mkdir(parents=True, exist_ok=True)
            (yolo_dir / split / "labels").mkdir(parents=True, exist_ok=True)
        
        # Collect images and create dataset.yaml
        classes = {"helmet": 0, "no_helmet": 1}
        image_paths = []
        labels = []
        
        for class_name, class_id in classes.items():
            class_dir = data_root / class_name
            if class_dir.exists():
                for img_path in class_dir.glob("*.[jp][pn]g"):
                    image_paths.append(img_path)
                    labels.append(class_id)
        
        # Split dataset
        train_paths, val_paths, train_labels, val_labels = train_test_split(
            image_paths, labels, test_size=1-train_split, random_state=42
        )
        
        # Create dataset.yaml
        dataset_yaml = {
            'path': str(yolo_dir),
            'train': 'train/images',
            'val': 'val/images',
            'nc': 2,
            'names': {0: 'helmet', 1: 'no_helmet'}
        }
        
        dataset_yaml_path = yolo_dir / "dataset.yaml"
        with open(dataset_yaml_path, 'w') as f:
            yaml.dump(dataset_yaml, f)
        
        logger.info(f"Dataset prepared. Train: {len(train_paths)}, Val: {len(val_paths)}")
        logger.info(f"Dataset YAML saved to {dataset_yaml_path}")
        
        return str(dataset_yaml_path)
    
    def train(self, dataset_yaml: str, epochs: int = 100, batch_size: int = 16, 
              img_size: int = 640, patience: int = 20):
        """
        Train YOLOv8 model for helmet detection.
        
        Args:
            dataset_yaml: Path to dataset.yaml file
            epochs: Number of training epochs
            batch_size: Batch size for training
            img_size: Input image size
            patience: Early stopping patience
        """
        logger.info("Starting YOLOv8 Helmet Detection Training")
        
        # Load model
        model = YOLO("yolov8m.pt")  # Use yolov8m (medium) model
        
        # Train model
        results = model.train(
            data=dataset_yaml,
            epochs=epochs,
            imgsz=img_size,
            batch=batch_size,
            patience=patience,
            device=self.device,
            project="models/helmet_detection",
            name="helmet_detector",
            save=True,
            half=True if self.device == "cuda" else False,
            optimizer='SGD',
            lr0=0.01,
            lrf=0.01,
            momentum=0.937,
            weight_decay=0.0005,
            warmup_epochs=3.0,
            warmup_momentum=0.8,
            warmup_bias_lr=0.1,
            box=7.5,
            cls=0.5,
            dfl=1.5,
            verbose=True
        )
        
        logger.info("Training completed successfully")
        return model, results
    
    def evaluate(self, model, test_images_dir: str):
        """
        Evaluate model performance on test set.
        
        Args:
            model: Trained YOLO model
            test_images_dir: Directory containing test images
        """
        logger.info(f"Evaluating model on test set from {test_images_dir}")
        
        metrics = {
            'total_images': 0,
            'helmet': 0,
            'no_helmet': 0,
            'detections': 0
        }
        
        for img_path in Path(test_images_dir).glob("*.[jp][pn]g"):
            results = model.predict(source=str(img_path), conf=0.5, verbose=False)
            metrics['total_images'] += 1
            
            for result in results:
                if result.boxes is not None:
                    for box in result.boxes:
                        class_id = int(box.cls[0])
                        if class_id == 0:
                            metrics['helmet'] += 1
                        else:
                            metrics['no_helmet'] += 1
                        metrics['detections'] += 1
        
        logger.info(f"Evaluation results:")
        for key, value in metrics.items():
            logger.info(f"  {key}: {value}")
        
        return metrics
    
    def export_model(self, model, export_format: str = "onnx"):
        """
        Export trained model to different formats.
        
        Args:
            model: Trained YOLO model
            export_format: Export format (onnx, torchscript, tflite, etc.)
        """
        logger.info(f"Exporting model to {export_format} format")
        path = model.export(format=export_format)
        logger.info(f"Model exported to {path}")
        return path


def main():
    parser = argparse.ArgumentParser(description="Train YOLOv8 Helmet Detection Model")
    parser.add_argument("--data", type=str, default="data/helmet", help="Path to helmet dataset")
    parser.add_argument("--epochs", type=int, default=100, help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=16, help="Batch size")
    parser.add_argument("--img-size", type=int, default=640, help="Input image size")
    parser.add_argument("--config", type=str, default="config/config.yaml", help="Config file path")
    parser.add_argument("--eval-only", action="store_true", help="Only evaluate without training")
    
    args = parser.parse_args()
    
    # Initialize trainer
    trainer = HelmetDetectionTrainer(config_path=args.config)
    
    if not args.eval_only:
        # Prepare dataset
        dataset_yaml = trainer.prepare_dataset(args.data)
        
        # Train model
        model, results = trainer.train(
            dataset_yaml=dataset_yaml,
            epochs=args.epochs,
            batch_size=args.batch_size,
            img_size=args.img_size
        )
        
        # Export model
        trainer.export_model(model, export_format="onnx")
    
    logger.info("Helmet detection model training pipeline completed!")


if __name__ == "__main__":
    main()
