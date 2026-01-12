import sys
import os
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from support_agent.agent import SupportAgent
from google.adk.events import Event
from google.genai import types
from google.adk.runners import InMemoryRunner

def main():
    # Load env vars
    load_dotenv(os.path.join(os.path.dirname(__file__), '../support_agent/.env'))
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY not found in support_agent/.env")
        return

    print("Initializing SupportAgent...")
    try:
        agent = SupportAgent(name="manual_test_agent", model="gemini-pro-latest")
    except Exception as e:
        print(f"Failed to initialize agent: {e}")
        return

    print("Agent initialized. Setting up Runner...")
    
    try:
        runner = InMemoryRunner(agent=agent)
        # Create session
        session_id = "test_session_live"
        user_id = "test_user_live"
        runner.session_service.create_session_sync(session_id=session_id, user_id=user_id, app_name="InMemoryRunner")
        
        print("Sending query...")
        user_query = "List all product collections available in the store."
        
        events = list(runner.run(
            user_id=user_id,
            session_id=session_id,
            new_message=types.Content(parts=[types.Part(text=user_query)])
        ))
        
        print("\n--- Agent Response Events ---")
        for event in events:
            if event.author == "manual_test_agent":
                print(f"\n[Agent]:")
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        print(part.text)
                else:
                    print("(No text content)")
            elif event.author == "user":
                print(f"\n[User]: {user_query}")
            else:
                print(f"\n[Other Event]: {event.author} - {type(event)}")
            
    except Exception as e:
        print(f"\nError during agent execution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
