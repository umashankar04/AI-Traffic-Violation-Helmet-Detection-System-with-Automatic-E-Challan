"""
E-Challan Generation and Management Service
"""

import logging
import random
import string
from datetime import datetime, timedelta
from typing import Optional
from backend.app.models.database import (
    Challan, ChallanStatusEnum, Violation, ViolationTypeEnum
)

logger = logging.getLogger(__name__)


class EChallanService:
    """
    Service for generating and managing electronic challans
    """
    
    @staticmethod
    def generate_challan_number() -> str:
        """
        Generate unique E-challan number.
        Format: ECH-YYYYMMDD-XXXXX
        """
        date_str = datetime.now().strftime("%Y%m%d")
        random_str = ''.join(random.choices(string.digits, k=5))
        return f"ECH-{date_str}-{random_str}"
    
    @staticmethod
    def create_challan(
        violation_id: int,
        violation: Violation,
        owner_name: str = None,
        owner_phone: str = None,
        owner_email: str = None,
        evidence_image_url: str = None,
        auto_issue: bool = False
    ) -> Challan:
        """
        Create E-challan from violation.
        
        Args:
            violation_id: ID of violation
            violation: Violation object
            owner_name: Vehicle owner name
            owner_phone: Owner phone number
            owner_email: Owner email
            evidence_image_url: URL to evidence image
            auto_issue: Whether to auto-issue immediately
            
        Returns:
            Challan object
        """
        # Get penalty for violation type
        from backend.app.services.violation_detection import ViolationDetectionService
        penalty = ViolationDetectionService.get_violation_penalty(violation.violation_type)
        
        # Calculate payment deadline (15 days)
        payment_deadline = datetime.utcnow() + timedelta(days=15)
        
        challan = Challan(
            challan_number=EChallanService.generate_challan_number(),
            status=ChallanStatusEnum.ISSUED if auto_issue else ChallanStatusEnum.ISSUED,
            violation_id=violation_id,
            violation_type=violation.violation_type,
            violation_timestamp=violation.timestamp,
            owner_name=owner_name or "Unknown",
            owner_phone=owner_phone,
            owner_email=owner_email,
            registration_number=violation.vehicle_number,
            penalty_amount=penalty,
            payment_deadline=payment_deadline,
            violation_location=violation.location_name,
            latitude=violation.latitude,
            longitude=violation.longitude,
            evidence_image_url=evidence_image_url or violation.image_path
        )
        
        logger.info(f"Created challan {challan.challan_number} for violation {violation_id}")
        return challan
    
    @staticmethod
    def mark_as_served(challan: Challan) -> Challan:
        """Mark challan as served."""
        challan.status = ChallanStatusEnum.SERVED
        challan.served_date = datetime.utcnow()
        logger.info(f"Marked challan {challan.challan_number} as served")
        return challan
    
    @staticmethod
    def record_payment(
        challan: Challan,
        amount: float,
        payment_method: str = "ONLINE",
        transaction_id: str = None
    ) -> Challan:
        """
        Record payment for challan.
        
        Args:
            challan: Challan to update
            amount: Payment amount
            payment_method: Payment method (ONLINE, OFFLINE, etc.)
            transaction_id: Transaction ID
            
        Returns:
            Updated challan
        """
        challan.paid_amount = amount
        challan.payment_method = payment_method
        challan.payment_date = datetime.utcnow()
        challan.transaction_id = transaction_id
        
        if amount >= challan.penalty_amount:
            challan.status = ChallanStatusEnum.PAID
        
        logger.info(f"Recorded payment of {amount} for challan {challan.challan_number}")
        return challan
    
    @staticmethod
    def get_challan_details(challan: Challan) -> dict:
        """Get formatted challan details."""
        return {
            'challan_number': challan.challan_number,
            'status': challan.status.value,
            'violation_type': challan.violation_type.value,
            'violation_date': challan.violation_timestamp.isoformat(),
            'location': challan.violation_location,
            'vehicle_number': challan.registration_number,
            'owner_name': challan.owner_name,
            'owner_phone': challan.owner_phone,
            'owner_email': challan.owner_email,
            'penalty_amount': challan.penalty_amount,
            'paid_amount': challan.paid_amount,
            'balance_amount': max(0, challan.penalty_amount - challan.paid_amount),
            'payment_deadline': challan.payment_deadline.isoformat() if challan.payment_deadline else None,
            'evidence_image_url': challan.evidence_image_url,
            'issued_date': challan.issued_date.isoformat()
        }


class ChallanNotificationService:
    """
    Service for sending challan notifications
    """
    
    @staticmethod
    def send_email_notification(
        email: str,
        challan: Challan,
        template: str = "default"
    ) -> bool:
        """
        Send challan notification via email.
        
        Args:
            email: Recipient email
            challan: Challan to notify about
            template: Email template to use
            
        Returns:
            True if sent successfully
        """
        try:
            # TODO: Integrate with email service (SendGrid, AWS SES, etc.)
            logger.info(f"Email notification sent to {email} for challan {challan.challan_number}")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False
    
    @staticmethod
    def send_sms_notification(
        phone: str,
        challan: Challan
    ) -> bool:
        """
        Send challan notification via SMS.
        
        Args:
            phone: Recipient phone number
            challan: Challan to notify about
            
        Returns:
            True if sent successfully
        """
        try:
            # TODO: Integrate with SMS service (Twilio, AWS SNS, etc.)
            message = (
                f"E-Challan Alert: Violation detected for vehicle {challan.registration_number}. "
                f"Challan No: {challan.challan_number}. Penalty: Rs.{challan.penalty_amount}. "
                f"Pay by: {challan.payment_deadline.strftime('%Y-%m-%d')}"
            )
            logger.info(f"SMS notification sent to {phone}: {message}")
            return True
        except Exception as e:
            logger.error(f"Failed to send SMS: {str(e)}")
            return False
    
    @staticmethod
    def send_notifications(challan: Challan, email: str = None, phone: str = None) -> dict:
        """
        Send all configured notifications for a challan.
        
        Args:
            challan: Challan to notify about
            email: Email address (optional)
            phone: Phone number (optional)
            
        Returns:
            Dictionary with notification status
        """
        results = {
            'email_sent': False,
            'sms_sent': False
        }
        
        if email:
            results['email_sent'] = ChallanNotificationService.send_email_notification(
                email, challan
            )
        
        if phone:
            results['sms_sent'] = ChallanNotificationService.send_sms_notification(
                phone, challan
            )
        
        return results
