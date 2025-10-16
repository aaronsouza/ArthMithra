import os
from langchain_openai import ChatOpenAI
from typing import List, Dict, Any

# --- 1. Agent Initialization ---
# The agent initializes the LLM. It will automatically use the OPENAI_API_KEY
# from the .env file loaded by the main app.py.
try:
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
except Exception as e:
    # This provides a fallback if the API key is not set, preventing a crash.
    print(f"Warning: Could not initialize OpenAI LLM. Error: {e}")
    llm = None

# --- 2. Persona and Context Definition ---
# This section defines the different "personalities" the agent can adopt.
# The specific time and location context is embedded here.
personas = {
    "Friendly Advisor": (
        "You are a friendly and warm financial advisor from SmartLoan3D60X. "
        "Your goal is to make the user feel comfortable. Use simple language and be encouraging. "
        "For your reference, you are based in Hanamkonda, Telangana, India, and the current time is "
        "around 12:09 PM on Thursday, October 16, 2025. You can start the conversation by saying 'Hello from Hanamkonda!' or a similar greeting."
    ),
    "Financial Guru": (
        "You are a confident and knowledgeable financial expert from SmartLoan360X. "
        "You provide precise data and educational insights about loans and investments, "
        "referencing current Indian financial trends where possible."
    ),
    "Empathetic Listener": (
        "You are a soothing and patient assistant from SmartLoan360X. "
        "The user may be in a stressful situation (e.g., a medical loan). "
        "Prioritize empathy and reassurance above all else."
    ),
}


# --- 3. Life Event Detection Logic ---
def _detect_life_event(user_query: str) -> str:
    """A private helper function to detect keywords for life events."""
    query = user_query.lower()
    if any(keyword in query for keyword in ["married", "wedding", "marriage"]):
        return "marriage"
    if any(keyword in query for keyword in ["house", "apartment", "moving", "property"]):
        return "new_house"
    if any(keyword in query for keyword in ["medical", "hospital", "emergency", "doctor"]):
        return "medical_emergency"
    return None


# --- 4. Main Agent Execution Function ---
def run_sales_conversation(user_query: str, history: List[str], current_persona: str) -> Dict[str, Any]:
    """
    This is the core function of the sales agent. It takes the user's input,
    detects context, selects a persona, and generates a response.

    Args:
        user_query: The latest message from the user.
        history: The conversation history.
        current_persona: The persona the agent should currently use.

    Returns:
        A dictionary containing the AI's response and the persona that was used.
    """
    if not llm:
        return {
            "response": "I'm sorry, my AI brain is currently offline. Please check the API key configuration.",
            "persona_used": "Error"
        }

    # Step 1: Detect life events to dynamically change persona
    detected_event = _detect_life_event(user_query)
    if detected_event == "medical_emergency":
        persona_key = "Empathetic Listener"
    else:
        # If no specific event is detected, stick to the current persona
        persona_key = current_persona

    # Step 2: Select the system prompt based on the chosen persona
    system_prompt = personas.get(persona_key, personas["Friendly Advisor"])

    # Step 3: Construct the full prompt for the LLM
    conversation_history = "\n".join(history)
    full_prompt = (
        f"{system_prompt}\n\n"
        f"Previous Conversation:\n{conversation_history}\n\n"
        f"User: {user_query}\n"
        f"AI:"
    )

    # Step 4: Invoke the LLM to get the response
    ai_response = llm.invoke(full_prompt).content

    # Step 5: Return the result as a structured dictionary
    return {
        "response": ai_response,
        "persona_used": persona_key  # Return which persona was used for this turn
    }


# --- 5. Test Block ---
# This allows you to run this file directly to test the agent's logic.
if __name__ == '__main__':
    print("--- Testing Sales Agent ---")

    # Ensure you have a .env file with your OPENAI_API_KEY in the parent directory
    # or that the environment variable is set.
    from dotenv import load_dotenv

    # This looks for .env in the current or parent directory
    load_dotenv(dotenv_path='../.env')

    if not os.getenv("OPENAI_API_KEY"):
        print("FATAL: OPENAI_API_KEY is not set. Please create a .env file in the project root.")
    else:
        test_history = []

        # Test 1: Initial greeting
        print("\n--- Test 1: Initial Greeting ---")
        user_input = "Hello"
        result = run_sales_conversation(user_input, test_history, "Friendly Advisor")
        print(f"Persona: {result['persona_used']}")
        print(f"AI: {result['response']}")
        test_history.extend([f"User: {user_input}", f"AI: {result['response']}"])

        # Test 2: Medical emergency detection
        print("\n--- Test 2: Medical Emergency (Persona Shift) ---")
        user_input = "I need a loan urgently for a medical emergency."
        result = run_sales_conversation(user_input, test_history, "Friendly Advisor")
        print(f"Persona: {result['persona_used']}")  # Should have shifted to Empathetic Listener
        print(f"AI: {result['response']}")
