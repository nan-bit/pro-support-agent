# Build a Gemini Pro Customer Support Agent for Shopify

This guide will walk you through building a customer support agent for a Shopify e-commerce store using the Google Agent Development Kit (ADK) and the Gemini Pro model. The agent will be able to check order statuses, get product details, and retrieve customer information by interacting with the Shopify API.

## Prerequisites

- Python 3.8+
- An active Google Gemini API key.
- A Shopify store with Admin API access credentials.

## Project Structure

Here is the directory structure of the project you will be creating:

```
pro-support-agent/
├── requirements.txt
└── support_agent/
    ├── __init__.py
    ├── agent.py
    ├── tools.py
    └── .env
```

## Step 1: Create the Project Directory

First, create the main directory for your project.

```bash
mkdir pro-support-agent
cd pro-support-agent
```

## Step 2: Create the `requirements.txt` File

Create a `requirements.txt` file in the `pro-support-agent` directory and add the following dependencies:

```
google-adk
python-dotenv
google-generativeai
ShopifyAPI
```

## Step 3: Create the `support_agent` Directory and Files

Create the `support_agent` directory and the necessary Python files within it.

```bash
mkdir support_agent
touch support_agent/__init__.py
```

Now, let's add the code for `agent.py` and `tools.py`.

### `support_agent/agent.py`

This file contains the main logic for the agent, including its initialization, model, tools, and instructions.

```python
# agent.py
from google.adk.agents import LlmAgent
from google.adk.events import Event
from support_agent.tools import check_order_status, get_product_details, get_customer_info

class SupportAgent(LlmAgent):
    """A customer support agent that uses tools to handle order inquiries."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("SupportAgent initialized.")

    def perceive(self, event: Event) -> None:
        """Receives an event from the user and adds it to the conversation history."""
        self.add_event_to_history(event)

    def act(self) -> Event:
        """Calls the LLM to generate a response based on the conversation history."""
        response_event = self.llm.generate_content(self.history)
        self.add_event_to_history(response_event)
        return response_event

root_agent = SupportAgent(

    name="support_agent",

    model="gemini-pro-latest",

            tools=[
                check_order_status,
                get_product_details,
                get_customer_info,
            ],

    instruction="You are a helpful customer support agent for an e-commerce store. Use the provided tools to check order statuses, get product details and retrieve customer information. Always ask for the necessary IDs (order, product, customer) when performing an action."

)
```

### `support_agent/tools.py`

This file defines the tools that the agent can use to interact with the Shopify API.

```python
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
```

## Step 4: Set Up Environment Variables

Create a `.env` file inside the `support_agent` directory to store your API keys and Shopify credentials. You can do this by running the following command, which will create the file with the necessary placeholder content.

```bash
cat <<EOF > support_agent/.env
GOOGLE_API_KEY="YOUR_API_KEY"
SHOPIFY_SHOP_URL="your-store-name.myshopify.com"
SHOPIFY_API_VERSION="YYYY-MM"
SHOPIFY_API_ACCESS_TOKEN="your-admin-api-access-token"
EOF
```

After running this command, you still need to open the `support_agent/.env` file and replace the placeholder values with your actual credentials.

## Step 5: Install Dependencies and Run the Application

**1. Create and Activate a Python Virtual Environment**

- On macOS/Linux:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- On Windows:
  ```bash
  python -m venv venv
  .\venv\Scripts\activate
  ```

**2. Install Dependencies**

Install the required Python packages from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

**3. Run the Agent Web UI**

From the root directory of the project (`pro-support-agent`), run the ADK web server:

```bash
venv/bin/adk web .
```

**4. Access the Web UI**

Once the server is running, you will see a message like `Uvicorn running on http://127.0.0.1:8000`. Open your web browser and navigate to:

```
http://127.0.0.1:8000
```

You can now interact with your customer support agent through the chat interface.
