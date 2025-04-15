"""
Lemon License
A simple Lemon Squeezy license manager for Python applications.

Author: Umut Erhan, 2025
"""

import requests
from typing import Dict, Optional, Tuple, Any, Union
import platform

class LemonLicense:
    """
    A simple Lemon Squeezy license manager for Python applications.
    """
    
    API_URL = "https://api.lemonsqueezy.com/v1/licenses"
    
    def __init__(self, debug: bool = False):
        """
        Initialize the license manager.
        
        Args:
            debug: Whether to print debug information (default: False)
        """
        self.debug = debug
    
    def _generate_instance_name(self) -> str:
        """Generate a unique instance name based on system information."""
        system_info = {
            "system": platform.system(),
            "node": platform.node(),
            "machine": platform.machine(),
            "processor": platform.processor()
        }
        
        if self.debug:
            print(f"*Lemon License: Generating instance name: {system_info}")
            
        return f"{system_info['system']}_{system_info['node']}_{system_info['machine']}"
    
    def activate(self, license_key: str, instance_name: Optional[str] = None) -> Tuple[bool, Union[Dict[str, Any], str]]:
        """
        Activate a license key.
        
        Args:
            license_key: The license key to activate
            instance_name: Custom instance name (optional)
            
        Returns:
            Tuple containing (success, result_or_error_message)
            If successful, result is a dict with license information
            If failed, result is an error message string
        """
        if not instance_name:
            instance_name = self._generate_instance_name()
        
        data = {
            "license_key": license_key,
            "instance_name": instance_name
        }
        
        try:
            response = requests.post(
                f"{self.API_URL}/activate",
                data=data,
                headers={"Accept": "application/json"}
            )
            
            result = response.json()
            
            if self.debug:
                print(f"*Lemon License: Activation result: \n\n{result}\n")
            
            if result.get("activated", False):
                # Create license info response
                license_info = {
                    "license_key": license_key,
                    "instance_id": result.get("instance", {}).get("id"),
                    "status": result.get("license_key", {}).get("status"),
                    "expires_at": result.get("license_key", {}).get("expires_at"),
                    "product_name": result.get("meta", {}).get("product_name")
                }
                
                return True, license_info
            else:
                error_msg = result.get("error", "Unknown error occurred during activation")
                return False, error_msg
                
        except Exception as e:
            return False, f"Activation failed: {str(e)}"
    
    def validate(self, license_key: str, instance_id: Optional[str] = None) -> Tuple[bool, Union[Dict[str, Any], str]]:
        """
        Validate a license.
        
        Args:
            license_key: The license key to validate
            instance_id: The instance ID to validate (optional)
            
        Returns:
            Tuple containing (is_valid, result_or_error_message)
            If valid, result is a dict with license information including the valid flag
            If invalid, result is an error message string
        """
        # Check if we have the necessary data
        if not license_key:
            return False, "No license key provided"
        
        # Prepare data for API call
        data = {"license_key": license_key}
        if instance_id:
            data["instance_id"] = instance_id
        
        try:
            response = requests.post(
                f"{self.API_URL}/validate",
                data=data,
                headers={"Accept": "application/json"}
            )
            
            result = response.json()
            
            if self.debug:
                print(f"*Lemon License: Validation result: \n\n{result}\n")
            
            is_valid = result.get("valid", False)
            
            if is_valid:
                # Get license information
                license_info = {
                    "valid": True,  # Explicitly include the valid flag
                    "product_name": result.get("meta", {}).get("product_name"),
                    "status": result.get("license_key", {}).get("status"),
                    "expires_at": result.get("license_key", {}).get("expires_at"),
                    "customer_name": result.get("meta", {}).get("customer_name"),
                    "customer_email": result.get("meta", {}).get("customer_email")
                }
                
                return True, license_info
            else:
                error_msg = result.get("error", "License validation failed")
                return False, error_msg
                
        except Exception as e:
            return False, f"Validation failed: {str(e)}"
    
    def deactivate(self, license_key: str, instance_id: str) -> Tuple[bool, str]:
        """
        Deactivate a license.
        
        Args:
            license_key: The license key to deactivate
            instance_id: The instance ID to deactivate
            
        Returns:
            Tuple containing (success, message)
        """
        # Check if we have the necessary data
        if not license_key:
            return False, "No license key provided"
            
        if not instance_id:
            return False, "No instance ID provided"
        
        data = {
            "license_key": license_key,
            "instance_id": instance_id
        }
        
        try:
            response = requests.post(
                f"{self.API_URL}/deactivate",
                data=data,
                headers={"Accept": "application/json"}
            )
            
            result = response.json()
            
            if self.debug:
                print(f"*Lemon License: Deactivation result: \n\n{result}\n")
            
            if result.get("deactivated", False):
                return True, "License deactivated successfully"
            else:
                error_msg = result.get("error", "Unknown error occurred during deactivation")
                return False, error_msg
                
        except Exception as e:
            return False, f"Deactivation failed: {str(e)}"
            
    def is_licensed(self, license_key: str, instance_id: Optional[str] = None) -> bool:
        """
        Quick check if the application is licensed.
        
        Args:
            license_key: The license key to check
            instance_id: The instance ID to check (optional)
            
        Returns:
            True if license is valid, False otherwise
        """
        is_valid, _ = self.validate(license_key, instance_id)
        return is_valid 