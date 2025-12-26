"""
Database models for Traffic Violation Detection System
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()


class ViolationTypeEnum(str, enum.Enum):
    """Types of violations"""
    HELMET_NOT_WORN = "HELMET_NOT_WORN"
    TRIPLE_RIDING = "TRIPLE_RIDING"
    SIGNAL_VIOLATION = "SIGNAL_VIOLATION"
    SPEED_VIOLATION = "SPEED_VIOLATION"


class ViolationSeverityEnum(str, enum.Enum):
    """Severity levels"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ChallanStatusEnum(str, enum.Enum):
    """Challan status"""
    ISSUED = "ISSUED"
    SERVED = "SERVED"
    PAID = "PAID"
    DISPUTED = "DISPUTED"
    CANCELLED = "CANCELLED"


class Violation(Base):
    """
    Traffic Violation Record
    """
    __tablename__ = "violations"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Violation details
    violation_type = Column(Enum(ViolationTypeEnum), nullable=False)
    severity = Column(Enum(ViolationSeverityEnum), default=ViolationSeverityEnum.MEDIUM)
    description = Column(Text)
    
    # Location & Time
    latitude = Column(Float)
    longitude = Column(Float)
    location_name = Column(String(255))
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Vehicle Details
    vehicle_number = Column(String(20), index=True)
    vehicle_type = Column(String(50))  # Two-wheeler, Four-wheeler, etc.
    
    # Evidence
    image_path = Column(String(500))
    video_segment_path = Column(String(500))
    
    # Detection Confidence
    detection_confidence = Column(Float, default=0.0)
    
    # Linked Challan
    challan_id = Column(Integer)
    
    # Status
    is_processed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Violation(id={self.id}, type={self.violation_type}, vehicle={self.vehicle_number})>"


class Challan(Base):
    """
    Electronic Challan (Fine Notice)
    """
    __tablename__ = "challans"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Challan Details
    challan_number = Column(String(50), unique=True, index=True)
    status = Column(Enum(ChallanStatusEnum), default=ChallanStatusEnum.ISSUED)
    
    # Violation Reference
    violation_id = Column(Integer, nullable=False)
    violation_type = Column(Enum(ViolationTypeEnum))
    violation_timestamp = Column(DateTime)
    
    # Owner Details
    owner_name = Column(String(255))
    owner_phone = Column(String(20))
    owner_email = Column(String(255))
    registration_number = Column(String(20))
    
    # Fine Details
    penalty_amount = Column(Float, nullable=False)
    payment_deadline = Column(DateTime)
    paid_amount = Column(Float, default=0.0)
    
    # Evidence
    evidence_image_url = Column(String(500))
    
    # Location Details
    violation_location = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Payment Info
    payment_method = Column(String(50))  # ONLINE, OFFLINE, etc.
    payment_date = Column(DateTime)
    transaction_id = Column(String(100))
    
    # Notifications
    email_sent = Column(Boolean, default=False)
    sms_sent = Column(Boolean, default=False)
    
    # Timestamps
    issued_date = Column(DateTime, default=datetime.utcnow)
    served_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Challan(id={self.id}, number={self.challan_number}, status={self.status})>"


class ViolationHeatmapData(Base):
    """
    Aggregated violation data for heatmap visualization
    """
    __tablename__ = "heatmap_data"
    
    id = Column(Integer, primary_key=True, index=True)
    
    latitude = Column(Float, index=True)
    longitude = Column(Float, index=True)
    
    violation_count = Column(Integer, default=0)
    violation_type = Column(Enum(ViolationTypeEnum))
    
    # Time aggregation
    date = Column(DateTime, index=True)
    hour = Column(Integer)  # 0-23
    
    severity_score = Column(Float, default=0.0)  # Higher = more severe area
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<HeatmapData(lat={self.latitude}, lng={self.longitude}, count={self.violation_count})>"


class CameraLocation(Base):
    """
    Registered CCTV Camera Locations
    """
    __tablename__ = "camera_locations"
    
    id = Column(Integer, primary_key=True, index=True)
    
    camera_id = Column(String(50), unique=True, index=True)
    camera_name = Column(String(255))
    
    latitude = Column(Float)
    longitude = Column(Float)
    location_name = Column(String(255))
    
    rtsp_url = Column(String(500))  # RTSP stream URL
    is_active = Column(Boolean, default=True)
    
    # Coverage details
    coverage_area = Column(String(255))
    road_name = Column(String(255))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<CameraLocation(id={self.camera_id}, name={self.camera_name})>"


class ProcessingQueue(Base):
    """
    Queue for video/image processing
    """
    __tablename__ = "processing_queue"
    
    id = Column(Integer, primary_key=True, index=True)
    
    source_path = Column(String(500), nullable=False)
    source_type = Column(String(20))  # IMAGE, VIDEO
    camera_id = Column(String(50))
    
    status = Column(String(50), default="PENDING")  # PENDING, PROCESSING, COMPLETED, FAILED
    priority = Column(Integer, default=0)
    
    processed_at = Column(DateTime)
    error_message = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<ProcessingQueue(id={self.id}, status={self.status})>"
