import unittest
from unittest.mock import MagicMock, patch
import sys
import os
from typing import AsyncGenerator, Optional

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from support_agent.agent import SupportAgent
from google.adk.events import Event
from google.adk.models.base_llm import BaseLlm
from google.adk.models.llm_response import LlmResponse
from google.adk.models.llm_request import LlmRequest
from google.adk.runners import InMemoryRunner
from google.genai import types

class MockLlm(BaseLlm):
    """A mock LLM that returns predefined responses."""
    model: str = "mock-model"
    response_text: str = ""
    last_request: Optional[LlmRequest] = None
    
    def __init__(self, response_text: str):
        super().__init__(model="mock-model", response_text=response_text)

    async def generate_content_async(
        self, llm_request: LlmRequest, stream: bool = False
    ) -> AsyncGenerator[LlmResponse, None]:
        self.last_request = llm_request
        response = LlmResponse(
            content=types.Content(
                parts=[types.Part(text=self.response_text)]
            )
        )
        yield response

class TestSupportAgentMock(unittest.TestCase):
    def setUp(self):
        self.mock_llm = MockLlm(response_text="The order is paid and fulfilled.")
        # Override the model with our mock
        self.agent = SupportAgent(name="test_agent", model=self.mock_llm)
        
    @patch('support_agent.tools.get_order_status')
    def test_agent_run_calls_llm(self, mock_get_order_status):
        # Setup runner
        runner = InMemoryRunner(agent=self.agent)
        
        # Create session
        runner.session_service.create_session_sync(session_id="session1", user_id="user1", app_name="InMemoryRunner")
        
        # Run agent
        events = list(runner.run(
            user_id="user1",
            session_id="session1",
            new_message=types.Content(parts=[types.Part(text="Check status of order #1001")])
        ))
        
        # Verify LLM was called
        self.assertIsNotNone(self.mock_llm.last_request)
        # Verify response event is in the output
        found_response = False
        for event in events:
            if event.author == "test_agent" and event.content and event.content.parts:
                if "The order is paid and fulfilled." in event.content.parts[0].text:
                    found_response = True
                    break
        self.assertTrue(found_response, "Agent response not found in events")

if __name__ == '__main__':
    unittest.main()
