# Gemini Pro Customer Support Agent

This project demonstrates a customer support agent built using the Google Agent Development Kit (ADK) and powered by the Gemini Pro model. The agent is designed for an e-commerce platform and can handle various customer inquiries by using a set of predefined tools.

## Features

The support agent can perform the following actions:
- **Check Order Status:** Provide the current status of an order (e.g., "Shipped", "Processing").
- **Cancel Orders:** Cancel an order if it has not yet been shipped.
- **Initiate Returns:** Start the return process for a shipped order.
- **Get Product Details:** Retrieve information about a product, including its name, price, and inventory level.
- **Retrieve Customer Information:** Look up a customer's name and email address.
- **Update Product Inventory:** Modify the inventory count for a specific product.

## Prerequisites

- Python 3.8+
- An active Google Gemini API key.

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

**4. Set Up Your Gemini API Key**
You need to create a `.env` file to store your Gemini API key securely.

- Create the file inside the `support_agent` directory:
  ```bash
  touch support_agent/.env
  ```
- Open `support_agent/.env` in a text editor and add your API key as follows:
  ```
  GOOGLE_API_KEY="YOUR_API_KEY"
  ```
- Replace `"YOUR_API_KEY"` with your actual Gemini API key and save the file.

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
    ├── tools.py      # Defines the tools the agent can use
    └── .env          # (To be created) Stores the API key
```
- **`agent.py`**: Initializes the `LlmAgent`, defines its model, tools, and instructions.
- **`tools.py`**: Contains all the functions that the agent can call to interact with the e-commerce store's data (e.g., `check_order_status`, `get_product_details`).
- **`requirements.txt`**: Lists the Python dependencies for the project.