# Gemini Pro Customer Support Agent

This project demonstrates a customer support agent built using the Google Agent Development Kit (ADK) and powered by the Gemini Pro model. The agent is designed for a Shopify-based e-commerce platform and can handle various customer inquiries by using a set of predefined tools that interact with the Shopify API.

## Features

The support agent can perform the following actions by interacting with the Shopify API:
- **Check Order Status:** Provide the current status of a Shopify order.
- **Get Product Details:** Retrieve information about a product from Shopify, including its name, status, vendor, and type. It can find products by both Product ID and Variant ID.
- **Retrieve Customer Information:** Look up a customer's name, email, and total order count from Shopify.

## Prerequisites

- Python 3.8+
- An active Google Gemini API key.
- A Shopify store with Admin API access credentials.

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
You need to create a `.env` file to store your API keys and Shopify credentials securely.

- Create the file inside the `support_agent` directory:
  ```bash
  touch support_agent/.env
  ```
- Open `support_agent/.env` in a text editor and add your credentials as follows:
  ```
  GOOGLE_API_KEY="YOUR_API_KEY"
  SHOPIFY_SHOP_URL="your-store-name.myshopify.com"
  SHOPIFY_API_VERSION="YYYY-MM"
  SHOPIFY_API_ACCESS_TOKEN="your-admin-api-access-token"
  ```
- Replace the placeholder values with your actual credentials and save the file.

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
    ├── tools.py      # Defines the tools that interact with the Shopify API
    └── .env          # (To be created) Stores API keys and credentials
```
- **`agent.py`**: Initializes the `LlmAgent`, defines its model, tools, and instructions.
- **`tools.py`**: Contains all the functions that the agent can call to interact with the Shopify store's data (e.g., `check_order_status`, `get_product_details`).
- **`requirements.txt`**: Lists the Python dependencies for the project.