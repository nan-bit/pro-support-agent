# debug_shopify.py

import os
from dotenv import load_dotenv
import shopify

# --- Load Environment Variables ---
# Make sure this points to your .env file
dotenv_path = os.path.join(os.path.dirname(__file__), 'support_agent', '.env')
load_dotenv(dotenv_path=dotenv_path)

print("Attempting to connect to Shopify...")

# --- Get Credentials ---
shop_url = os.getenv("SHOPIFY_SHOP_URL")
api_version = os.getenv("SHOPIFY_API_VERSION")
access_token = os.getenv("SHOPIFY_API_ACCESS_TOKEN")

# --- !! IMPORTANT !! ---
# PASTE THE VARIANT ID YOU ARE TESTING HERE
TEST_VARIANT_ID = "42684296888394" 
# -----------------------

# --- Validation ---
if not all([shop_url, api_version, access_token]):
    print("🔴 ERROR: Shopify credentials are not fully set in the .env file.")
    exit()

print(f"Shop URL: {shop_url}")
print(f"API Version: {api_version}")

try:
    # --- Activate Session ---
    session = shopify.Session(shop_url, api_version, access_token)
    shopify.ShopifyResource.activate_session(session)
    
    print(f"\n🔍 Searching for Variant with ID: {TEST_VARIANT_ID}...")
    
    # --- Make the API Call ---
    variant = shopify.Variant.find(TEST_VARIANT_ID)
    
    # --- Check the Result ---
    if variant:
        print("\n✅ SUCCESS: Found Variant!")
        print(f"   - Title: {variant.title}")
        print(f"   - Product ID: {variant.product_id}")
    else:
        print(f"\n🟡 WARNING: No variant found with ID {TEST_VARIANT_ID}. The ID might be incorrect or not accessible.")

except Exception as e:
    print(f"\n🔴 ERROR: An exception occurred during the API call.")
    print(f"   - Details: {e}")
    print("\n   - Troubleshooting:")
    print("     1. Double-check your SHOPIFY_API_ACCESS_TOKEN.")
    print("     2. Ensure your custom app has 'read_products' permission.")
    print("     3. Check your SHOPIFY_API_VERSION. Try using '2024-04'.")

finally:
    # --- Clean Up Session ---
    if 'shopify' in locals():
        shopify.ShopifyResource.clear_session()
        print("\nDisconnected from Shopify.")
