"""
Airtable service module.
Handles interactions with Airtable API for data operations using the airtable library.
"""

import os
import logging
from typing import Dict, Any
from airtable import Airtable

# Configure logging
logger = logging.getLogger(__name__)

class AirtableService:
    """Service class for Airtable API interactions using the airtable library."""
    
    def __init__(self):
        """Initialize Airtable service with API credentials."""
        self.api_key = os.getenv("AIRTABLE_API_KEY")
        self.base_id = os.getenv("AIRTABLE_BASE_ID")
        
        if not self.api_key:
            raise ValueError("AIRTABLE_API_KEY not found in environment variables")
        if not self.base_id:
            raise ValueError("AIRTABLE_BASE_ID not found in environment variables")
        
        self.client = Airtable(base_id=self.base_id, api_key=self.api_key)

    def create_record(self, table_name: str, fields: Dict[str, Any]) -> Any:
        """
        Create a new record in an Airtable table.
        
        Args:
            table_name: Name of the Airtable table
            fields: Record fields to create
            
        Returns:
            Created record data
        """
        try:
            record = self.client.create(table_name, fields)
            return record
            
        except Exception as e:
            logger.error(f"Error creating record in Airtable table '{table_name}': {str(e)}")
            raise

# Factory function to create AirtableService instances
def create_airtable_service() -> AirtableService:
    """
    Factory function to create AirtableService instances.
    This is the recommended approach for serverless environments.
    
    Returns:
        New AirtableService instance
    """
    return AirtableService() 