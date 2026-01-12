# Gemini Pro Customer Support Agent

This project demonstrates an advanced customer support agent built using the Google Agent Development Kit (ADK) and powered by the Gemini Pro model. The agent is designed for a Shopify-based e--commerce platform and can handle a wide variety of customer inquiries by using a set of predefined tools that interact with both the Shopify and Stripe APIs.

## Features

The support agent can perform the following actions by interacting with Shopify and Stripe APIs:
- **Check Order Status:** Provide the current financial and fulfillment status of a Shopify order.
- **Get Product Details:** Retrieve information about a product, including its variants and IDs.
- **Retrieve Customer Information:** Look up a customer's name, email, and total order count.
- **Browse Product Collections:** List all available product collections and show the products within a specific collection.
- **Create Checkout Links:** Help customers purchase an item by generating a secure Shopify checkout link for a specific product.
- **Check Payment Details (Stripe):** Retrieve payment status, amount, and payment method for an order processed through Stripe.
- **Process Refunds (Stripe):** Issue full or partial refunds for an order directly via the Stripe API.

## Prerequisites

- Python 3.8+
- An active Google Gemini API key.
- A Shopify store with Admin API access credentials.
- A Stripe account with API access keys, used as the payment processor in the Shopify store.

## Setup and Installation

Follow these steps to set up and run the project on your local machine.

**1. Clone the Repository**
```bash
git clone https://github.com/nan-bit/pro-support-agent.git
cd pro-support-agent
```

**2. Create and Activate a Python Virtual Environment**
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

**3. Install Dependencies**
Install the required Python packages from the `requirements.txt` file.
```bash
pip install -r requirements.txt
```

**4. Set Up Your Environment Variables**
You need to create a `.env` file to store your API keys and credentials securely.

- Create the file inside the `support_agent` directory:
  ```bash
  touch support_agent/.env
  ```
- Open `support_agent/.env` in a text editor and add your credentials as follows:
  ```
  GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
  SHOPIFY_SHOP_URL="your-store-name.myshopify.com"
  SHOPIFY_API_VERSION="YYYY-MM"
  SHOPIFY_API_ACCESS_TOKEN="your-admin-api-access-token"
  STRIPE_API_KEY="sk_test_YOUR_STRIPE_SECRET_KEY"
  ```
- Replace the placeholder values with your actual credentials and save the file.

## Shopify App Configuration

To allow the agent to use its tools, you must grant the correct permissions to your custom Shopify App.

1.  In your Shopify Admin, go to **Apps** > **App and sales channel settings** > **Develop apps for your store**.
2.  Click on your custom app.
3.  Navigate to the **Configuration** tab and edit the **Admin API integration** scopes.
4.  Ensure the following permissions are checked:
    - `read_products`
    - `read_product_listings`
    - `read_customers`
    - `read_orders`
    - `write_orders` (Required for processing refunds)
    - `read_draft_orders` (Required for creating checkout links)
    - `write_draft_orders` (Required for creating checkout links)
5.  Click **Save**.

## Running the Application

**1. Run the Agent Web UI**
From the root directory of the project (`pro-support-agent`), run the ADK web server:
```bash
venv/bin/adk web .
```

**2. Access the Web UI**
Once the server is running, you will see a message like `Uvicorn running on http://127.0.0.1:8000`. Open your web browser and navigate to:
```
http://127.0.0.1:8000
```

You can now interact with the customer support agent through the chat interface.

## Project Structure
```
.
├── .gitignore
├── requirements.txt
└── support_agent/
    ├── __init__.py
    ├── agent.py      # Main agent logic and definition
    ├── tools.py      # Defines tools that interact with Shopify & Stripe APIs
    └── .env          # (To be created) Stores API keys and credentials
```
- **`agent.py`**: Initializes the `LlmAgent`, defines its model, tools, and instructions.
- **`tools.py`**: Contains all the functions that the agent can call to interact with the Shopify store's data and process payments with Stripe.
- **`requirements.txt`**: Lists the Python dependencies for the project.