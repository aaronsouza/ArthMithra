import streamlit as st
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Dict, Any
import os
from PIL import Image
from datetime import datetime
from dotenv import load_dotenv

# --- 0. Environment Setup ---
# This line loads the environment variables from your .env file.
load_dotenv()

# Create a directory for file uploads if it doesn't exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# --- 1. LLM & Persona Configuration ---

# Initialize the Large Language Model. It will automatically use the
# OPENAI_API_KEY loaded from your .env file.
try:
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
except Exception as e:
    st.error(
        f"Failed to initialize OpenAI LLM. Please make sure your OPENAI_API_KEY is set correctly in the .env file. Error: {e}")
    st.stop()

# Define the AI personas. The "Friendly Advisor" now includes the specific time/location context.
personas = {
    "Friendly Advisor": f"You are a friendly and warm financial advisor from SmartLoan360X, located in Hanamkonda, Telangana, India. Your goal is to make the user feel comfortable. Use simple language, be encouraging. For your reference, the current time is Thursday, October 16, 2025 at 11:59 AM IST. Greet the user and subtly mention the time.",
    "Financial Guru": "You are a confident and knowledgeable financial expert from SmartLoan360X. You provide precise data and educational insights about loans and investments, referencing current Indian financial trends where possible.",
    "Empathetic Listener": "You are a soothing and patient assistant from SmartLoan360X. The user may be in a stressful situation (e.g., a medical loan). Prioritize empathy and reassurance above all else.",
    "Data-Driven Analyst": "You are a precise, technical analyst. You present loan offers, terms, and conditions clearly and without emotional language. You are direct and focus on the numbers.",
}


def get_llm_response(persona_key: str, user_query: str, history: List[str], additional_context: str = ""):
    """Helper function to invoke the LLM with a specific persona and conversation history."""
    system_prompt = personas.get(persona_key, personas["Friendly Advisor"])

    conversation = "\n".join(history)
    prompt = f"{system_prompt}\n\nPrevious Conversation:\n{conversation}\n\n{additional_context}\n\nUser: {user_query}\nAI:"

    response = llm.invoke(prompt)
    return response.content


# --- 2. Simulated Agent & Tool Functions ---
# These functions mimic the behavior of specialized agents and tools.

def life_event_detector(user_query: str) -> str:
    """Simulates the Life Event Predictor Agent by detecting keywords."""
    query = user_query.lower()
    if any(keyword in query for keyword in ["married", "wedding", "marriage"]):
        return "marriage"
    if any(keyword in query for keyword in ["house", "apartment", "moving", "property"]):
        return "new_house"
    if any(keyword in query for keyword in ["medical", "hospital", "emergency", "doctor"]):
        return "medical_emergency"
    return None


def extract_text_from_image(image_path: str) -> Dict[str, Any]:
    """Simulates the Vision-Based KYC & OCR Agent. This is a dummy function."""
    filename = os.path.basename(image_path).lower()
    if "aadhar" in filename:
        return {"doc_type": "Aadhar", "name": "Priya Sharma", "dob": "10-05-1992", "aadhar_no": "1234 5678 9012"}
    if "pan" in filename:
        return {"doc_type": "PAN", "name": "Priya Sharma", "pan_no": "ABCDE1234F"}

    return {"error": "Could not recognize document type."}


def run_underwriting_check(customer_data: Dict[str, Any]) -> Dict[str, Any]:
    """Simulates the Underwriting & Risk Agent and calculates the Financial Health Index (FHI)."""
    credit_score = customer_data.get("credit_score", 720)
    income = customer_data.get("income", 800000)

    fhi = 0
    if credit_score > 750:
        fhi += 40
    elif credit_score > 680:
        fhi += 30
    else:
        fhi += 10

    if income > 1000000:
        fhi += 40
    elif income > 500000:
        fhi += 30
    else:
        fhi += 20

    fhi += 15  # Dummy repayment habit score

    decision = {"fhi_score": fhi}
    if fhi > 65:
        decision.update(
            {"approved": True, "reason": "Strong FHI score.", "interest_rate": "10.5%", "loan_amount": "500,000 INR"})
    elif fhi > 40:
        decision.update(
            {"approved": True, "reason": "Moderate FHI score.", "interest_rate": "12.5%", "loan_amount": "250,000 INR"})
    else:
        decision.update({"approved": False, "reason": "Low FHI score. Suggest credit improvement plan."})

    return decision


def generate_sanction_letter(customer_name: str, loan_details: Dict[str, Any]) -> str:
    """Simulates the Sanction Letter Agent."""
    letter_content = f"""
    **Loan Sanction Letter**

    Date: {datetime.now().strftime('%d-%b-%Y')}

    Dear {customer_name},

    We are pleased to inform you that your loan has been approved!

    - **Approved Amount**: {loan_details['loan_amount']}
    - **Interest Rate**: {loan_details['interest_rate']}

    Thank you for choosing SmartLoan360X.
    """
    return letter_content


# --- 3. LangGraph State & Workflow Definition ---

class AppState(TypedDict):
    customer_query: str
    conversation_history: List[str]
    customer_data: Dict[str, Any]
    current_persona: str
    underwriting_result: Dict[str, Any]
    final_response: str
    task_is_done: bool


# --- 4. LangGraph Nodes (Agent Steps) ---

def sales_node(state: AppState):
    st.session_state.current_agent = "💬 Sales & Negotiation Agent"
    query = state["customer_query"]
    history = state["conversation_history"]
    persona = state["current_persona"]

    event = life_event_detector(query)
    additional_context = ""
    if event == "marriage":
        additional_context = "Context: The user mentioned getting married. Gently guide them towards a personal loan for wedding expenses or a home loan."
        state["current_persona"] = "Friendly Advisor"
    elif event == "medical_emergency":
        additional_context = "Context: The user mentioned a medical emergency. Be extremely empathetic. Offer a quick personal loan for medical expenses."
        state["current_persona"] = "Empathetic Listener"

    response = get_llm_response(persona, query, history, additional_context)
    state["conversation_history"].extend([f"User: {query}", f"AI: {response}"])
    state["final_response"] = response
    return state


def kyc_node(state: AppState):
    st.session_state.current_agent = "🕵️‍♂️ Vision-Based KYC Agent"
    filepath = state["customer_data"].get("uploaded_file_path")
    if not filepath:
        state["final_response"] = "There was an error with the file upload. Please try again."
        return state

    ocr_result = extract_text_from_image(filepath)
    if "error" in ocr_result:
        state["final_response"] = f"KYC Failed: {ocr_result['error']}. Please upload a clear Aadhar or PAN card image."
        state["task_is_done"] = True
    else:
        state["customer_data"].update(ocr_result)
        state["customer_data"]["kyc_verified"] = True
        state[
            "final_response"] = f"Thank you! We've successfully verified your {ocr_result['doc_type']}. Name: {ocr_result['name']}. Proceeding with underwriting."
    return state


def underwriting_node(state: AppState):
    st.session_state.current_agent = "🧮 Underwriting & Risk Agent"
    result = run_underwriting_check(state["customer_data"])
    state["underwriting_result"] = result
    state["customer_data"]["fhi_score"] = result.get("fhi_score")
    return state


def approval_node(state: AppState):
    st.session_state.current_agent = "✅ Approval Agent"
    state["current_persona"] = "Data-Driven Analyst"
    details = state["underwriting_result"]
    context = f"Context: The user's loan is approved. Present this offer: {details}"
    response = get_llm_response(state["current_persona"], "Present the approved loan offer.", [], context)
    state["final_response"] = response
    return state


def rejection_node(state: AppState):
    st.session_state.current_agent = "❌ Rejection & Guidance Agent"
    state["current_persona"] = "Empathetic Listener"
    details = state["underwriting_result"]["reason"]
    fhi = state["customer_data"]["fhi_score"]
    context = f"Context: The user's loan was not approved because: '{details}'. Their FHI is {fhi}. Gently inform them and suggest a credit improvement plan."
    response = get_llm_response(state["current_persona"], "Inform user about loan rejection and provide guidance.", [],
                                context)
    state["final_response"] = response
    state["task_is_done"] = True
    return state


def sanction_letter_node(state: AppState):
    st.session_state.current_agent = "🧾 Sanction Letter Agent"
    query = state["customer_query"].lower()
    if "yes" in query or "generate" in query or "accept" in query:
        letter = generate_sanction_letter(state["customer_data"]["name"], state["underwriting_result"])
        response = f"Excellent! Here is your sanction letter:\n\n---\n{letter}\n---\n\nWhat's next? I can offer some financial literacy tips."
    else:
        response = "No problem. Let me know if you change your mind. Would you like some financial literacy tips?"
    state["final_response"] = response
    return state


def education_node(state: AppState):
    st.session_state.current_agent = "🧑‍🏫 Financial Education Coach"
    state["current_persona"] = "Financial Guru"
    context = "Context: Provide 3 concise, actionable tips on managing debt responsibly."
    response = get_llm_response(state["current_persona"], "Provide financial tips.", [], context)
    state["final_response"] = response
    state["task_is_done"] = True
    return state


# --- 5. LangGraph Conditional Edges (Routing Logic) ---

def route_after_underwriting(state: AppState):
    return "approval" if state["underwriting_result"].get("approved") else "rejection"


def route_after_sanction_letter(state: AppState):
    query = state["customer_query"].lower()
    return "education" if "yes" in query or "tips" in query else END


# --- 6. Graph Construction ---

workflow = StateGraph(AppState)
workflow.add_node("sales", sales_node)
workflow.add_node("kyc", kyc_node)
workflow.add_node("underwriting", underwriting_node)
workflow.add_node("approval", approval_node)
workflow.add_node("rejection", rejection_node)
workflow.add_node("sanction_letter", sanction_letter_node)
workflow.add_node("education", education_node)

workflow.set_entry_point("sales")
workflow.add_edge("sales", END)
workflow.add_edge("kyc", "underwriting")
workflow.add_conditional_edge("underwriting", route_after_underwriting,
                              {"approval": "approval", "rejection": "rejection"})
workflow.add_edge("approval", "sanction_letter")
workflow.add_edge("rejection", END)
workflow.add_conditional_edge("sanction_letter", route_after_sanction_letter, {"education": "education", END: END})
workflow.add_edge("education", END)
app = workflow.compile()

# --- 7. Streamlit User Interface ---

st.set_page_config(page_title="SmartLoan360X", page_icon="🧠", layout="wide")
st.title("🧠 SmartLoan360X — Agentic Financial Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "graph_state" not in st.session_state:
    st.session_state.graph_state = AppState(
        customer_query="", conversation_history=[], customer_data={},
        current_persona="Friendly Advisor", underwriting_result={},
        final_response="", task_is_done=False
    )
if "current_agent" not in st.session_state:
    st.session_state.current_agent = "Idle"

col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("Conversational AI")
    chat_container = st.container(height=500)
    for msg in st.session_state.messages:
        with chat_container.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("How can I help you today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container.chat_message("user"): st.markdown(prompt)

        current_state = st.session_state.graph_state
        current_state["customer_query"] = prompt

        with st.spinner(f"Thinking... Agent in charge: {st.session_state.current_agent}"):
            final_state = app.invoke(current_state)
            st.session_state.graph_state = final_state

        response = final_state.get("final_response", "Sorry, an issue occurred.")
        st.session_state.messages.append({"role": "assistant", "content": response})
        with chat_container.chat_message("assistant"): st.markdown(response)

with col2:
    st.subheader("System Status & Controls")
    st.info(f"**Current Agent:** {st.session_state.current_agent}")
    with st.expander("🔑 Customer Data", expanded=True):
        st.json(st.session_state.graph_state.get("customer_data", {}))
    with st.expander("📄 KYC Document Upload", expanded=True):
        uploaded_file = st.file_uploader("Upload Aadhar or PAN Card", type=["png", "jpg", "jpeg"])
        if uploaded_file is not None:
            file_path = os.path.join("uploads", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"Uploaded {uploaded_file.name}")

            st.session_state.messages.append(
                {"role": "user", "content": f"System: Uploaded '{uploaded_file.name}' for KYC."})
            current_state = st.session_state.graph_state
            current_state["customer_data"]["uploaded_file_path"] = file_path

            with st.spinner("Processing KYC..."):
                kyc_state = kyc_node(current_state)
                st.session_state.graph_state = kyc_state
                if kyc_state["customer_data"].get("kyc_verified"):
                    underwriting_state = underwriting_node(kyc_state)
                    decision = route_after_underwriting(underwriting_state)
                    final_state = approval_node(underwriting_state) if decision == "approval" else rejection_node(
                        underwriting_state)
                    st.session_state.graph_state = final_state
                else:
                    final_state = kyc_state

            response = final_state.get("final_response", "KYC processing complete.")
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

    with st.expander("🧠 AI Persona Control", expanded=False):
        selected_persona = st.selectbox(
            "Manually select AI Persona",
            options=list(personas.keys()),
            index=list(personas.keys()).index(st.session_state.graph_state["current_persona"])
        )
        if selected_persona != st.session_state.graph_state["current_persona"]:
            st.session_state.graph_state["current_persona"] = selected_persona
            st.rerun()

if not st.session_state.messages:
    initial_state = st.session_state.graph_state
    initial_state["customer_query"] = "Hello"
    with st.spinner("Initializing..."):
        final_state = app.invoke(initial_state)
    st.session_state.graph_state = final_state
    st.session_state.messages.append({"role": "assistant", "content": final_state['final_response']})
    st.rerun()

