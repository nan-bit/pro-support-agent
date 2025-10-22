# tools.py
import os
import shopify
from dotenv import load_dotenv
load_dotenv()

# --- Shopify API Connection Setup ---
shop_url = os.getenv("SHOPIFY_SHOP_URL")
api_version = os.getenv("SHOPIFY_API_VERSION")
access_token = os.getenv("SHOPIFY_API_ACCESS_TOKEN")

if not all([shop_url, api_version, access_token]):
    raise ValueError("Shopify credentials are not fully set in the .env file.")

# Activate the Shopify API session
session = shopify.Session(shop_url, api_version, access_token)
shopify.ShopifyResource.activate_session(session)
# ------------------------------------

def check_order_status(order_number: str) -> str:
    """Checks the financial and fulfillment status of a Shopify order by its number (e.g., #1001)."""
    print(f"Tool: Searching for Shopify order number {order_number}")
    try:
        # The 'name' field in the Shopify API corresponds to the order number like #1001
        orders = shopify.Order.find(name=order_number)
        if not orders:
            return f"Order {order_number} not found."
        
        order = orders[0] # Get the first result
        return (f"Status for Order {order.name}: "
                f"Financial Status is '{order.financial_status}', "
                f"Fulfillment Status is '{order.fulfillment_status}'.")
    except Exception as e:
        return f"An error occurred while fetching order status: {e}"
    finally:
        shopify.ShopifyResource.clear_session()

def get_product_details(item_id: str) -> str:
    """Retrieves details for a product, accepting either a Product ID or a Variant ID."""
    print(f"Tool: Getting details for Shopify item ID {item_id}")
    try:
        # First, try to find it as a Product
        product = shopify.Product.find(item_id)
        if product:
            return (f"Product Found: '{product.title}'. "
                    f"Status: {product.status}, Vendor: {product.vendor}, Type: {product.product_type}.")

    except Exception:
        # If it fails, it might be a Variant ID. Let's try that.
        print(f"Tool: Could not find Product with ID {item_id}. Trying as a Variant ID.")
        try:
            variant = shopify.Variant.find(item_id)
            if variant:
                # If we find a variant, we can get the parent product's info
                product = shopify.Product.find(variant.product_id)
                return (f"Found Variant '{variant.title}' which belongs to Product '{product.title}'. "
                        f"Product Status: {product.status}, Vendor: {product.vendor}, Type: {product.product_type}.")
        except Exception:
            # If both fail, then it truly can't be found.
            pass

    return f"Could not find any product or variant with the ID {item_id}."

def get_customer_info(customer_id: str) -> str:
    """Retrieves customer information by their unique customer ID."""
    print(f"Tool: Getting info for Shopify customer ID {customer_id}")
    try:
        customer = shopify.Customer.find(customer_id)
        if not customer:
            return f"Customer with ID {customer_id} not found."
        
        return (f"Customer Found: {customer.first_name} {customer.last_name}, "
                f"Email: {customer.email}, Total Orders: {customer.orders_count}.")
    except Exception as e:
        return f"An error occurred while fetching customer info: {e}"
    finally:
        shopify.ShopifyResource.clear_session()

# Note: The tool functions for cancel_order, return_order, and update_product_inventory
# would require 'write' permissions (e.g., write_orders) and are more complex.
# We are focusing on the 'read' functions for this demo.