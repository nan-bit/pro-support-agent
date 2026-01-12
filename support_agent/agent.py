# support_agent/agent.py

from google.adk.agents import LlmAgent
from google.adk.events import Event
from support_agent.tools import (
    get_order_status,
    get_product_details,
    get_customer_info,
    get_all_collections,
    get_products_in_collection,
    create_checkout_link
)

class SupportAgent(LlmAgent):
    """A customer support agent that uses tools to handle order inquiries."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("SupportAgent initialized.")

    # act and perceive methods removed as they are handled by the Runner


root_agent = SupportAgent(

    name="support_agent",

    model="gemini-pro-latest",

    # Provide the agent with its complete set of tools
    tools=[
        get_order_status,
        get_product_details,
        get_customer_info,
        get_all_collections,
        get_products_in_collection,
        create_checkout_link,
    ],

    # Give the agent a comprehensive set of instructions for all its capabilities
    instruction=(
        "You are a helpful and friendly customer support agent for an e-commerce store. "
        "Your primary goal is to assist customers by using the provided tools. "
        "You can check order statuses, look up product details, find customer information, and list products in a collection. "
        "You can also help customers make a purchase by using the `create_checkout_link` tool. "
        "Always be clear and confirm necessary details like IDs (order, product, customer) before taking action."
    )
)