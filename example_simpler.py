from lemon_license import LemonLicense

# Initialize without app_name, with debug set to False
license_manager = LemonLicense(debug=False)
license_key = "5AD5D964-FBC2-4FF8-81D2-9AC4A78EE46D"

premium_features = "amazing premium feature"

is_valid, result = license_manager.validate(license_key)

if is_valid:
    print(f"✅ {premium_features} is available")
else:
    print(f"❌ Basic features only: \n\'{result}\'")
