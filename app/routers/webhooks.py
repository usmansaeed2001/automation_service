"""
Webhooks router.
Handles webhooks for various services.
"""
from fastapi import APIRouter, HTTPException
import logging
from typing import Dict, Any

from app.services.airtable import create_airtable_service

# Configure logging
logger = logging.getLogger(__name__)

# Create router instance
router = APIRouter()

@router.post("/kajabi/process-form-submission")
async def kajabi_process_form_submission(payload: Dict[str, Any]):
    """
    Process Kajabi form submission webhook.
    This endpoint is used to process form submissions from Kajabi.
    It logs the received webhook data and triggers appropriate automation workflows.
    """
    try:
        # Log the received webhook data
        logger.info(f"Received Kajabi webhook: {payload.get('event_type', 'unknown')}")
        logger.info(f"Webhook data: {payload.get('data', {})}")
        
        airtable_service = create_airtable_service()
        airtable_service.create_record("Form Submissions", payload.get('data', {}))
        # Here you would typically process the webhook data
        # and trigger appropriate automation workflows
        
        return {
            "status": "success",
            "message": "Webhook received and logged",
            "event_type": payload.get('event_type', 'unknown')
        }
        
    except Exception as e:
        logger.error(f"Error processing Kajabi webhook: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
