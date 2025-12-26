"""
Phase 2: Number Plate Detection & OCR Module
YOLOv8 for plate detection + EasyOCR/Tesseract for text extraction
"""

import logging
import re
import cv2
import numpy as np
from pathlib import Path
from ultralytics import YOLO
import easyocr
import torch

logger = logging.getLogger(__name__)


class NumberPlateDetector:
    """
    Detects vehicle number plates in images/videos using YOLOv8
    """
    
    def __init__(self, model_path: str, conf_threshold: float = 0.4, device: str = None):
        """
        Initialize number plate detector.
        
        Args:
            model_path: Path to trained YOLO model
            conf_threshold: Confidence threshold
            device: 'cuda' or 'cpu'
        """
        self.conf_threshold = conf_threshold
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        
        logger.info(f"Loading number plate detection model from {model_path}")
        self.model = YOLO(model_path)
        self.model.to(self.device)
    
    def detect(self, image: np.ndarray, return_crops: bool = True) -> dict:
        """
        Detect number plates in image.
        
        Args:
            image: Input image (BGR)
            return_crops: If True, return cropped plate regions
            
        Returns:
            Dictionary with detections
        """
        results = self.model.predict(source=image, conf=self.conf_threshold, verbose=False)
        
        detections = {
            'plates': [],
            'raw_results': results
        }
        
        for result in results:
            if result.boxes is not None:
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    conf = float(box.conf[0])
                    
                    detection = {
                        'bbox': (x1, y1, x2, y2),
                        'confidence': conf,
                        'area': (x2 - x1) * (y2 - y1)
                    }
                    
                    if return_crops:
                        # Add padding for better OCR
                        padding = 10
                        x1_pad = max(0, x1 - padding)
                        y1_pad = max(0, y1 - padding)
                        x2_pad = min(image.shape[1], x2 + padding)
                        y2_pad = min(image.shape[0], y2 + padding)
                        detection['crop'] = image[y1_pad:y2_pad, x1_pad:x2_pad].copy()
                    
                    detections['plates'].append(detection)
        
        return detections
    
    def draw_detections(self, image: np.ndarray, detections: dict, 
                       ocr_results: dict = None) -> np.ndarray:
        """
        Draw detected plates on image.
        
        Args:
            image: Input image
            detections: Detection results
            ocr_results: OCR results if available
            
        Returns:
            Image with drawn detections
        """
        output = image.copy()
        
        for idx, detection in enumerate(detections['plates']):
            x1, y1, x2, y2 = detection['bbox']
            conf = detection['confidence']
            
            # Draw bounding box
            cv2.rectangle(output, (x1, y1), (x2, y2), (0, 255, 0), 2)
            
            # Add confidence and OCR text if available
            label = f"Plate {conf:.2f}"
            if ocr_results and idx < len(ocr_results['texts']):
                plate_text = ocr_results['texts'][idx]
                label += f" | {plate_text}"
            
            cv2.putText(output, label, (x1, y1 - 5),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        return output


class PlateOCR:
    """
    Extract text from number plates using EasyOCR
    """
    
    # Indian number plate format: AB01XY1234
    INDIAN_PLATE_REGEX = r"^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$"
    
    def __init__(self, languages: list = None, device: str = None):
        """
        Initialize OCR reader.
        
        Args:
            languages: List of language codes (default: ['en'])
            device: 'cuda' or 'cpu'
        """
        self.languages = languages or ['en']
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        
        logger.info(f"Loading EasyOCR reader for languages: {self.languages}")
        self.reader = easyocr.Reader(self.languages, gpu=(self.device == "cuda"))
    
    def extract_text(self, image: np.ndarray, conf_threshold: float = 0.3) -> dict:
        """
        Extract text from plate image.
        
        Args:
            image: Cropped plate image
            conf_threshold: Confidence threshold for OCR
            
        Returns:
            Dictionary with OCR results
        """
        # Preprocess image for better OCR
        image_processed = self._preprocess_plate(image)
        
        # Perform OCR
        results = self.reader.readtext(image_processed)
        
        ocr_data = {
            'raw_text': '',
            'cleaned_text': '',
            'confidence': 0.0,
            'is_valid_indian_plate': False,
            'all_detections': []
        }
        
        if results:
            # Concatenate all detected texts
            texts = [detection[1] for detection in results if detection[2] > conf_threshold]
            raw_text = ''.join(texts).upper()
            
            # Clean and validate
            ocr_data['raw_text'] = raw_text
            ocr_data['cleaned_text'] = self._clean_text(raw_text)
            ocr_data['confidence'] = np.mean([d[2] for d in results if d[2] > conf_threshold])
            ocr_data['is_valid_indian_plate'] = self._validate_indian_plate(
                ocr_data['cleaned_text']
            )
            
            # Store all detections
            ocr_data['all_detections'] = results
        
        return ocr_data
    
    def _preprocess_plate(self, image: np.ndarray) -> np.ndarray:
        """
        Preprocess plate image for better OCR accuracy.
        
        Args:
            image: Input image
            
        Returns:
            Preprocessed image
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)
        
        # Denoise
        denoised = cv2.fastNlMeansDenoising(enhanced, h=10)
        
        # Threshold
        _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Optional: Morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        morph = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=1)
        
        return morph
    
    def _clean_text(self, text: str) -> str:
        """
        Clean OCR output to improve format validity.
        
        Args:
            text: Raw OCR text
            
        Returns:
            Cleaned text
        """
        # Remove spaces
        text = text.replace(' ', '')
        
        # Replace similar looking characters
        text = text.replace('O', '0')  # O -> 0
        text = text.replace('I', '1')  # I -> 1
        text = text.replace('Z', '2')  # Z -> 2
        text = text.replace('S', '5')  # S -> 5
        text = text.replace('B', '8')  # B -> 8
        
        return text.upper()
    
    def _validate_indian_plate(self, text: str) -> bool:
        """
        Validate if text matches Indian number plate format.
        
        Args:
            text: Cleaned text to validate
            
        Returns:
            True if valid Indian plate format
        """
        return bool(re.match(self.INDIAN_PLATE_REGEX, text))
    
    def extract_from_crops(self, plate_crops: list) -> dict:
        """
        Extract text from multiple plate crop images.
        
        Args:
            plate_crops: List of cropped plate images
            
        Returns:
            Dictionary with OCR results for each crop
        """
        results = {
            'plates': [],
            'valid_plates': [],
            'total_confidence': 0.0
        }
        
        for idx, crop in enumerate(plate_crops):
            ocr_result = self.extract_text(crop)
            results['plates'].append(ocr_result)
            
            if ocr_result['is_valid_indian_plate']:
                results['valid_plates'].append({
                    'index': idx,
                    'text': ocr_result['cleaned_text'],
                    'confidence': ocr_result['confidence']
                })
        
        if results['plates']:
            results['total_confidence'] = np.mean([p['confidence'] for p in results['plates']])
        
        return results


class NumberPlateRecognitionPipeline:
    """
    Complete pipeline for number plate detection and OCR
    """
    
    def __init__(self, plate_detector_model: str, ocr_languages: list = None):
        """
        Initialize complete recognition pipeline.
        
        Args:
            plate_detector_model: Path to trained plate detection model
            ocr_languages: Languages for OCR
        """
        self.plate_detector = NumberPlateDetector(plate_detector_model)
        self.ocr = PlateOCR(languages=ocr_languages)
    
    def process_image(self, image: np.ndarray) -> dict:
        """
        Process image: detect plates and extract text.
        
        Args:
            image: Input image
            
        Returns:
            Complete results with detections and OCR
        """
        # Detect plates
        detections = self.plate_detector.detect(image, return_crops=True)
        
        # Extract OCR from crops
        plate_crops = [d['crop'] for d in detections['plates']]
        ocr_results = self.ocr.extract_from_crops(plate_crops) if plate_crops else {}
        
        # Combine results
        results = {
            'detections': detections,
            'ocr': ocr_results,
            'plates_found': len(detections['plates']),
            'valid_plates_found': len(ocr_results.get('valid_plates', []))
        }
        
        return results
    
    def process_video(self, video_path: str, output_path: str = None) -> dict:
        """
        Process video and extract all number plates.
        
        Args:
            video_path: Path to video file
            output_path: Optional output video path
            
        Returns:
            Statistics and results
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
            'frames_with_plates': 0,
            'total_plates_detected': 0,
            'valid_indian_plates': 0,
            'all_plates': []
        }
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            stats['total_frames'] += 1
            
            # Process frame
            results = self.process_image(frame)
            
            if results['plates_found'] > 0:
                stats['frames_with_plates'] += 1
                stats['total_plates_detected'] += results['plates_found']
                stats['valid_indian_plates'] += results['valid_plates_found']
                
                # Store plate info
                for plate in results['ocr'].get('valid_plates', []):
                    stats['all_plates'].append({
                        'frame': stats['total_frames'],
                        'text': plate['text'],
                        'confidence': plate['confidence']
                    })
                
                # Draw on frame
                frame = self.plate_detector.draw_detections(
                    frame, results['detections'], results['ocr']
                )
            
            if writer:
                writer.write(frame)
        
        cap.release()
        if writer:
            writer.release()
        
        logger.info(f"Video processing completed: {stats}")
        return stats


if __name__ == "__main__":
    # Example usage
    pipeline = NumberPlateRecognitionPipeline(
        plate_detector_model="models/plate_detection/best.pt"
    )
    
    # Process image
    image = cv2.imread("test_image.jpg")
    results = pipeline.process_image(image)
    
    print(f"Plates found: {results['plates_found']}")
    print(f"Valid Indian plates: {results['valid_plates_found']}")
    for plate in results['ocr'].get('valid_plates', []):
        print(f"  {plate['text']} (confidence: {plate['confidence']:.2f})")
