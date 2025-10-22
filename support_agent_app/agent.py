# agent.py
from google.adk.agents import LlmAgent
from google.adk.events import Event
from support_agent_app.tools import check_order_status, cancel_order, return_order, get_product_details, get_customer_info, update_product_inventory

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

                cancel_order,

                return_order,

                get_product_details,

                get_customer_info,

                update_product_inventory,

            ],

    instruction="You are a helpful customer support agent for an e-commerce store. Use the provided tools to check order statuses, cancel orders, initiate returns, get product details, retrieve customer information, and update product inventory. Always ask for the necessary IDs (order, product, customer) when performing an action."

)
