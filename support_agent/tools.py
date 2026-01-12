# support_agent/tools.py

import os
import shopify
from dotenv import load_dotenv
load_dotenv()

# --- Load Credentials ---
SHOP_URL = os.getenv("SHOPIFY_SHOP_URL")
API_VERSION = os.getenv("SHOPIFY_API_VERSION")
ACCESS_TOKEN = os.getenv("SHOPIFY_API_ACCESS_TOKEN")

# --- Helper function to manage Shopify sessions ---
def activate_shopify_session():
    """Activates a new Shopify API session for a tool call."""
    session = shopify.Session(SHOP_URL, API_VERSION, ACCESS_TOKEN)
    shopify.ShopifyResource.activate_session(session)

# --- Tools ---

def get_order_status(order_number: str) -> str:
    """Checks the financial and fulfillment status of a Shopify order by its number (e.g., #1001)."""
    print(f"Tool: Searching for Shopify order number {order_number}")
    try:
        activate_shopify_session()
        orders = shopify.Order.find(name=order_number)
        if not orders:
            return f"Order {order_number} not found."
        order = orders[0]
        return (
            f"Status for Order {order.name}: "
            f"Financial Status is '{order.financial_status}', "
            f"Fulfillment Status is '{order.fulfillment_status}'."
        )
    except Exception as e:
        return f"An error occurred while fetching order status: {e}"
    finally:
        shopify.ShopifyResource.clear_session()

def get_product_details(item_id: str) -> str:
    """Retrieves details for a product, accepting either a Product ID or a Variant ID."""
    print(f"Tool: Getting details for Shopify item ID {item_id}")
    try:
        activate_shopify_session()
        # First, try to find it as a Variant, as it's more specific
        try:
            variant = shopify.Variant.find(item_id)
            if variant:
                product = shopify.Product.find(variant.product_id)
                return (
                    f"Found Variant '{variant.title}' (ID: {variant.id}) which belongs to "
                    f"Product '{product.title}' (ID: {product.id})."
                )
        except Exception:
            pass # If not a variant ID, proceed to check as a Product ID

        # If not found as a variant, try as a Product
        product = shopify.Product.find(item_id)
        if product:
            variants_info = ", ".join([f"{v.title} (Variant ID: {v.id})" for v in product.variants])
            return (
                f"Product Found: '{product.title}' (ID: {product.id}). "
                f"Status: {product.status}, Vendor: {product.vendor}. "
                f"Available Variants: [{variants_info}]."
            )

        return f"Could not find any product or variant with the ID {item_id}."
    except Exception as e:
        return f"An API error occurred while searching for item {item_id}: {e}"
    finally:
        shopify.ShopifyResource.clear_session()

# ... (Apply the same activate/finally pattern to all other Shopify tools) ...

def get_customer_info(customer_id: str) -> str:
    """Retrieves customer information by their unique customer ID."""
    print(f"Tool: Getting info for Shopify customer ID {customer_id}")
    try:
        activate_shopify_session()
        customer = shopify.Customer.find(customer_id)
        return (
            f"Customer Found: {customer.first_name} {customer.last_name}, "
            f"Email: {customer.email}, Total Orders: {customer.orders_count}."
        )
    except Exception as e:
        return f"Customer with ID {customer_id} not found or an error occurred: {e}"
    finally:
        shopify.ShopifyResource.clear_session()

def get_all_collections() -> str:
    """Retrieves all available smart collections in the Shopify store."""
    print("Tool: Getting all smart collections from Shopify")
    try:
        activate_shopify_session()
        collections = shopify.SmartCollection.find()
        if not collections: return "No smart collections found."
        collection_list = "\n".join([f"- {c.title} (ID: {c.id})" for c in collections])
        return f"Found the following collections:\n{collection_list}"
    except Exception as e:
        return f"An error occurred while fetching collections: {e}"
    finally:
        shopify.ShopifyResource.clear_session()

def get_products_in_collection(collection_id: str) -> str:
    """Retrieves all products within a specific collection by its ID."""
    print(f"Tool: Getting products for collection ID {collection_id}")
    try:
        activate_shopify_session()
        products = shopify.Product.find(collection_id=collection_id)
        if not products: return f"No products found in collection ID {collection_id}."
        product_list = "\n".join([f"- {p.title} (Status: {p.status})" for p in products])
        return f"Products in collection {collection_id}:\n{product_list}"
    except Exception as e:
        return f"An error occurred while fetching products: {e}"
    finally:
        shopify.ShopifyResource.clear_session()
        
def create_checkout_link(variant_id: str, quantity: int) -> str:
    """Creates a Shopify draft order and returns a secure checkout link for a given product variant_id and quantity."""
    print(f"Tool: Creating checkout link for variant {variant_id} with quantity {quantity}")
    try:
        activate_shopify_session()
        draft_order = shopify.DraftOrder()
        draft_order.line_items = [{"variant_id": variant_id, "quantity": quantity}]
        draft_order.save()

        if draft_order.errors:
            return f"Failed to create draft order. Errors: {draft_order.errors.full_messages()}"

        return f"Checkout link created successfully: {draft_order.invoice_url}"
    except Exception as e:
        return f"An error occurred while creating the checkout link: {e}"
    finally:
        shopify.ShopifyResource.clear_session()