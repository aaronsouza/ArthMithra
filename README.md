# ArthMithra

ArthMithra is a multi-agent AI system designed to transform the financial services landscape in India. Moving beyond simple chatbots, it functions as an autonomous Digital Relationship Manager (DRM), orchestrating specialized AI agents to manage the entire customer lifecycle—from sales and verification to financial education and long-term trust-building.

This project is not just about selling loans; it's about building lasting financial relationships through an intelligent, empathetic, and compliant AI ecosystem.

---

## 🧠 Core Idea: A Holistic, Human-Centric AI Banking Assistant
SmartLoan360X is an agentic AI system that combines financial intelligence, emotion modeling, and real-world awareness to handle sales, education, and customer well-being. It orchestrates multiple autonomous AI agents, each with a specialized skill set, to provide a seamless and deeply personalized customer experience.

---

## ✨ Key Features & Innovations

- **🧩 Financial Health Index (FHI):**  
  A proprietary score (based on credit history, savings trends, chat sentiment) to offer truly personalized guidance, moving from transactional sales to relationship-building.

- **🔐 Federated & Privacy-Preserving AI:**  
  Models are trained on distributed customer data without centralizing Personally Identifiable Information (PII), ensuring full compliance with RBI data localization laws.

- **🧬 Adaptive AI Personas:**  
  The AI dynamically shifts its tone and personality (e.g., Friendly Advisor, Financial Guru, Empathetic Listener) based on the customer's needs and context.

- **🧑‍💻 Vision-Based KYC & OCR Agent:**  
  Integrated Computer Vision agent extracts and verifies customer details from uploaded ID documents (Aadhar, PAN), reducing fraud and streamlining onboarding.

- **💬 Real-Time Market Intelligence:**  
  An agent monitors financial news and RBI rate changes (via mock APIs) to provide timely, context-aware offers and advice.

- **💡 Autonomous Self-Learning Loop:**  
  The system self-evaluates conversations to identify drop-off points, missed opportunities, and confusing dialogue, autonomously refining its prompts and strategies weekly.

---

## 🧱 System Architecture
The system is built on a multi-agent architecture where a **Master Agent** orchestrates a network of specialized worker agents. This modular design allows for complex, autonomous workflows. Orchestration can be managed using frameworks like **LangGraph, CrewAI, or AutoGen**.

### Agent Network

- **Master Agent (Orchestrator):**  
  Delegates tasks to the appropriate worker agent based on the conversational context.

- **Worker Agents:**
  - **Sales & Negotiation Agent:** Manages product inquiries and negotiates terms.
  - **Verification & KYC Agent:** Handles document uploads, performs OCR, and verifies customer identity using computer vision.
  - **Underwriting Agent:** Assesses risk and provides explainable credit decisions.
  - **Sanction Letter Agent:** Generates and delivers official PDF sanction letters.
  - **Financial Advisor Agent:** Offers personalized recommendations and explains complex financial concepts.
  - **Sentiment & Personality Agent:** Analyzes customer emotion to guide the Adaptive AI Persona layer.
  - **Fraud & Bias Agent:** Monitors for anomalies and ensures fair, unbiased decisions.
  - **Life Event Predictor Agent:** Predicts customer needs (e.g., home loan after marriage) from conversational cues.
  - **Financial Education Agent:** Provides post-loan financial planning tips and educational content.
  - **Analytics Agent:** Mines conversation logs for patterns to feed into the self-learning loop.

---

## 📂 Project Structure
ArthMithra/
├── agents/ # Each agent's logic is a Python file here
│ ├── sales_agent.py
│ ├── kyc_agent.py
│ ├── underwriting_agent.py
│ └── ... (other agents)
├── tools/ # Reusable functions (PDF generator, OCR, mock APIs)
│ ├── pdf_generator.py
│ ├── ocr_tool.py
│ └── api_mocks.py
├── data/ # Sample data, logs, and documents
│ ├── sample_pan.png
│ ├── sample_aadhar.jpg
│ └── conversation_logs.json
├── app.py # Main Streamlit application
└── requirements.txt # Python package dependencies

