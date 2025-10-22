# tools.py
# A simple in-memory database for the demo
_ORDERS = {
    "12345": {"status": "Shipped", "items": ["ADK T-Shirt"]},
    "67890": {"status": "Processing", "items": ["Gemini Mug"]},
}

_PRODUCTS = {
    "P101": {"name": "Gemini T-Shirt", "price": 25.00, "inventory": 100},
    "P102": {"name": "ADK Hoodie", "price": 45.00, "inventory": 50},
}

_CUSTOMERS = {
    "C001": {"name": "Alice Smith", "email": "alice@example.com"},
    "C002": {"name": "Bob Johnson", "email": "bob@example.com"},
}

def check_order_status(order_id: str) -> str:
    """Checks the status of a given order ID."""
    print(f"Tool: Checking status for order {order_id}")
    return _ORDERS.get(order_id, {}).get("status", "Order not found")

def cancel_order(order_id: str) -> str:
    """Cancels an order if it has not yet been shipped."""
    print(f"Tool: Attempting to cancel order {order_id}")
    order = _ORDERS.get(order_id)
    if not order:
        return "Order not found."
    if order["status"] == "Shipped":
        return "Cannot cancel order, it has already been shipped."
    order["status"] = "Cancelled"
    return "Order has been successfully cancelled."

def return_order(order_id: str) -> str:
    """Initiates a return for a shipped order."""
    print(f"Tool: Initiating return for order {order_id}")
    order = _ORDERS.get(order_id)
    if not order:
        return "Order not found."
    if order["status"] != "Shipped":
        return "Cannot initiate a return for an order that has not been shipped."
    return "Return initiated. Please check your email for a shipping label."

def get_product_details(product_id: str) -> str:
    """Retrieves details for a specific product by its ID."""
    print(f"Tool: Getting details for product {product_id}")
    product = _PRODUCTS.get(product_id)
    if not product:
        return "Product not found."
    return f"Product Name: {product['name']}, Price: ${product['price']:.2f}, Inventory: {product['inventory']}"

def get_customer_info(customer_id: str) -> str:
    """Retrieves customer information by customer ID."""
    print(f"Tool: Getting info for customer {customer_id}")
    customer = _CUSTOMERS.get(customer_id)
    if not customer:
        return "Customer not found."
    return f"Customer Name: {customer['name']}, Email: {customer['email']}"

def update_product_inventory(product_id: str, quantity: int) -> str:
    """Updates the inventory level for a specific product."""
    print(f"Tool: Updating inventory for product {product_id} to {quantity}")
    product = _PRODUCTS.get(product_id)
    if not product:
        return "Product not found."
    if quantity < 0:
        return "Inventory quantity cannot be negative."
    product['inventory'] = quantity
    return f"Inventory for {product['name']} updated to {quantity}."
