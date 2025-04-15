#!/usr/bin/env python3
"""
LemonLicense-Simple Example
A simple example showing how to use the LemonLicense module
"""

from lemon_license import LemonLicense
import sys

def display_menu():
    """Display the main menu options."""
    print("\nLemonLicense Example")
    print("=====================")
    print("1. Activate License")
    print("2. Validate License")
    print("3. Deactivate License")
    print("0. Exit")
    choice = input("\nEnter your choice (0-3): ")
    return choice


def main():
    # Initialize the license manager for this application
    license_manager = LemonLicense(app_name="ExampleApp", debug=True)
    
    # Variables to store license information for this session
    current_license_key = None
    current_instance_id = None
    
    while True:
        choice = display_menu()
        
        if choice == "0":
            print("Exiting...")
            break
            
        elif choice == "1":
            # Activate a license
            license_key = input("Enter your license key: ")
            if not license_key:
                print("No license key entered. Cancelling activation.")
                continue
                
            print("Activating license...")
            success, result = license_manager.activate(license_key)
            
            if success:
                # Store the license key and instance ID for this session
                current_license_key = license_key
                current_instance_id = result.get("instance_id")
                print(f"✅ License activated successfully for {result.get('product_name', 'Unknown')}")
                print(f"   Instance ID: {current_instance_id}")
                print("   Please save this instance ID if you need to deactivate the license later")
            else:
                print(f"❌ {result}")
                
        elif choice == "2":
            # Validate a license
            if current_license_key:
                print(f"Using current license key: {current_license_key[:8]}...")
                license_key = current_license_key
            else:
                license_key = input("Enter license key to validate: ")
                if not license_key:
                    print("No license key entered. Cancelling validation.")
                    continue
            
            # Use current instance ID if available
            instance_id = current_instance_id
            if not instance_id:
                instance_id = input("Enter instance ID (optional, press Enter to skip): ")
                instance_id = instance_id if instance_id else None
            
            print("Validating license...")
            is_valid, result = license_manager.validate(license_key, instance_id)
            
            if is_valid:
                print("\nLicense Information:")
                print("-------------------")
                print(f"Valid:        {result.get('valid', False)}")
                print(f"Product:      {result.get('product_name', 'N/A')}")
                print(f"Status:       {result.get('status', 'N/A')}")
                
                expires_at = result.get('expires_at')
                if expires_at:
                    print(f"Expires at:   {expires_at}")
                else:
                    print("Expires at:   Never")
                    
                print(f"Customer:     {result.get('customer_name', 'N/A')}")
                print(f"Email:        {result.get('customer_email', 'N/A')}")
            else:
                print(f"❌ {result}")
                
        elif choice == "3":
            # Deactivate a license
            if current_license_key and current_instance_id:
                print(f"Using current license key: {current_license_key[:8]}...")
                print(f"Using current instance ID: {current_instance_id}")
                license_key = current_license_key
                instance_id = current_instance_id
            else:
                license_key = input("Enter license key to deactivate: ")
                if not license_key:
                    print("No license key entered. Cancelling deactivation.")
                    continue
                
                instance_id = input("Enter instance ID: ")
                if not instance_id:
                    print("No instance ID entered. Cancelling deactivation.")
                    continue
            
            confirm = input("Are you sure you want to deactivate the license? (y/n): ")
            if confirm.lower() != 'y':
                print("Deactivation cancelled.")
                continue
                
            print("Deactivating license...")
            success, message = license_manager.deactivate(license_key, instance_id)
            
            if success:
                print(f"✅ {message}")
                # Clear the stored license information
                if license_key == current_license_key and instance_id == current_instance_id:
                    current_license_key = None
                    current_instance_id = None
            else:
                print(f"❌ {message}")
                
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main() 