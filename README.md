# Simple Lemon Squeezy License Manager

A simple Python module for integrating Lemon Squeezy license management into your applications.

## Features

- Lightweight (single file with minimal dependencies)
- Activate licenses with Lemon Squeezy
- Validate active licenses
- Deactivate licenses
- Simple integration with any Python application
- No external dependencies except for the requests library
- Optional debug mode for troubleshooting

## Requirements

- Python 3.6+
- `requests` library

## Installation

1. Copy the `lemon_license.py` file into your project
2. Install the required dependency: `pip install requests`

## Quick Start

The simplest way to use LemonLicense is for validating a license key:

```python
from lemon_license import LemonLicense

# Initialize the license manager
license_manager = LemonLicense(debug=False)
license_key = "YOUR-LICENSE-KEY-HERE"

premium_features = "amazing premium feature"

is_valid, result = license_manager.validate(license_key)

if is_valid:
    print(f"✅ {premium_features} is available")
else:
    print(f"❌ Basic features only: \n\'{result}\'")
```

## Usage

### Initialize the License Manager

```python
from lemon_license import LemonLicense

# Initialize with default settings
license_manager = LemonLicense()

# Initialize with debug mode for troubleshooting
license_manager = LemonLicense(debug=True)
```

### Activating a License

```python
# Get license key from user input
license_key = input("Enter your license key: ")

# Activate the license
success, result = license_manager.activate(license_key)
if success:
    print(f"License activated successfully for {result['product_name']}")
    print(f"Instance ID: {result['instance_id']}")
    # Save the instance_id for future validation/deactivation
else:
    print(f"License activation failed: {result}")
    
# You can also provide a custom instance name
success, result = license_manager.activate(license_key, instance_name="CustomInstanceName")
```

### Validating a License

```python
# Validate a license key (instance_id is optional)
license_key = "your-license-key"
instance_id = "your-instance-id"  # Optional

is_valid, result = license_manager.validate(license_key, instance_id)
if is_valid:
    # The 'valid' attribute is explicitly included in the result
    print(f"License valid: {result['valid']}")
    print(f"License is for product: {result['product_name']}")
    print(f"Status: {result['status']}")
    if result['expires_at']:
        print(f"Expires at: {result['expires_at']}")
    print(f"Licensed to: {result['customer_name']} ({result['customer_email']})")
else:
    print(f"License validation failed: {result}")

# Quick check if a license is valid
if license_manager.is_licensed(license_key, instance_id):
    print("License is valid")
else:
    print("License is invalid")
```

### Deactivating a License

```python
# Deactivate a license (both license_key and instance_id are required)
license_key = "your-license-key"
instance_id = "your-instance-id"

success, message = license_manager.deactivate(license_key, instance_id)
if success:
    print("License deactivated successfully")
else:
    print(f"License deactivation failed: {message}")
```

### Example Integration (Desktop Application)

Here's a simple example of integrating license validation into a desktop application:

```python
from lemon_license import LemonLicense
import json
import os

# Configuration file to store license information
CONFIG_FILE = "app_config.json"

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def main():
    # Initialize license manager
    license_manager = LemonLicense()
    
    # Load saved configuration (with license info)
    config = load_config()
    license_key = config.get("license_key")
    instance_id = config.get("instance_id")
    
    # Check if we have license info and if it's valid
    if license_key and license_manager.is_licensed(license_key, instance_id):
        print("Application is properly licensed")
    else:
        print("This application requires a valid license to run.")
        license_key = input("Enter your license key (or press Enter to exit): ")
        
        if not license_key:
            print("Exiting application.")
            return
            
        # Activate the license
        success, result = license_manager.activate(license_key)
        if not success:
            print(f"License activation failed: {result}")
            print("Exiting application.")
            return
        
        # Save the license information to config
        config["license_key"] = license_key
        config["instance_id"] = result["instance_id"]
        save_config(config)
        
        print(f"License activated successfully for {result['product_name']}")
    
    # Application is now licensed, continue with your main application logic
    print("Starting application...")
    # Your application code here...

if __name__ == "__main__":
    main()
```

### Example Integration (Web Server)

Here's an example of license validation in a Flask application:

```python
from flask import Flask, request, jsonify
from lemon_license import LemonLicense

app = Flask(__name__)
license_manager = LemonLicense()

@app.route('/api/data', methods=['GET'])
def get_data():
    # Get license key from request headers
    api_key = request.headers.get('X-License-Key')
    
    if not api_key:
        return jsonify({"error": "No license key provided"}), 401
    
    # Validate the license key
    is_valid, result = license_manager.validate(api_key)
    
    if not is_valid:
        return jsonify({"error": "Invalid license key", "details": result}), 403
    
    # The valid flag is explicitly included in the result for clarity
    # License is valid, continue with API logic
    return jsonify({
        "data": "Your requested data", 
        "license_valid": result.get('valid', True),
        "license_details": result
    })

if __name__ == '__main__':
    app.run(debug=True)
```

## License

This project is provided as-is under the MIT License.

## Author

Umut Erhan, 2025

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for the full changelog.

