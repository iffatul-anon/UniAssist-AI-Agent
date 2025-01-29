import os
import streamlit as st
from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv
from phi.tools.email import EmailTools
from phi.tools.googlesearch import GoogleSearch
from phi.tools.website import WebsiteTools
import fitz  # PyMuPDF for reading PDF files
import json  # To store and retrieve conversation history

# Load environment variables
load_dotenv()

# Sender Email Configuration
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_NAME = os.getenv("SENDER_NAME")
SENDER_PASSKEY = os.getenv("SENDER_PASSKEY")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# Define paths for conversation history
CONVERSATION_HISTORY_PATH = "conversation_history.json"

# Function to load conversation history
def load_conversation_history():
    if os.path.exists(CONVERSATION_HISTORY_PATH):
        with open(CONVERSATION_HISTORY_PATH, "r") as file:
            return json.load(file)
    return []

# Function to save conversation history
def save_conversation_history(history):
    with open(CONVERSATION_HISTORY_PATH, "w") as file:
        json.dump(history, file, indent=4)

# Load existing conversation history
conversation_history = load_conversation_history()

def load_conversation_history2():
    if os.path.exists("data.json"):
        with open("data.json", "r") as file:
            return json.load(file)
    return []

conversation = load_conversation_history2()

# Initialize the UniAssist Agent
uniassist_agent = Agent(
    name="UniAssist",
    role="Provide accurate and detailed responses for DIU-related queries.",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[
        GoogleSearch(),
    ],
    description=(
        "A virtual assistant specializing in academic support for Daffodil International University. "
        "It provides information on policies, courses, events, and general guidance."
    ),
    instructions=[
        "Respond concisely and accurately to user queries.",
        "If the user does not ask for specific information, act like a chatbot and engage in casual conversation.",
        "If additional resources are required, suggest them or search for the information using available tools.",
        "Structure responses clearly, using bullet points or paragraphs where necessary.",
    ],
    add_history_to_messages=True,
    show_tool_calls=True,
    markdown=True,
)

# Initialize the Email Agent
email_agent = Agent(
    name="EmailGen",
    role="Create professional and context-specific emails.",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[
        EmailTools(
            receiver_email=RECEIVER_EMAIL,
            sender_email=SENDER_EMAIL,
            sender_name=SENDER_NAME,
            sender_passkey=SENDER_PASSKEY,
        )
    ],
    description=(
        "An assistant for generating polished, professional emails tailored to user needs. "
        "Capable of drafting emails for administrative purposes, complaints, or inquiries."
    ),
    instructions=[
        "Draft polite, professional emails with correct grammar and formatting.",
        "Ensure the email includes a clear subject line, introduction, body, and closing.",
        "Seek user confirmation before finalizing or sending the email.",
        "Adapt the tone and structure of the email based on the context provided.",
    ],
    add_history_to_messages=True,
    show_tool_calls=True,
    markdown=True,
)

# Initialize the Search Agent
search_agent = Agent(
    name="SearchAgent",
    role="Provide structured and up-to-date job search results.",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[
        WebsiteTools(),
        GoogleSearch()
    ],
    description=(
        "A specialized search assistant designed to find the most relevant job, or opportunity listings. "
        "Capable of providing structured information such as job title, application deadline, and key requirements."
    ),
    instructions=[
        "Use the WebsiteTools to retrieve data from job portals when a relevant URL is provided.",
        "For job searches, extract and format the information into structured results including: \n"
        "  - Job Title\n"
        "  - Application Deadline\n"
        "  - Key Requirements",
        "Use Google Search only when more detailed information is required or if no direct portal data is provided.",
        "Summarize results concisely and provide actionable steps or links where appropriate.",
        "Present results in a user-friendly, bulleted or tabular format for clarity.",
        "Include only the most relevant and recent results for the user's query."
    ],
    add_history_to_messages=True,
    show_tool_calls=True,
    markdown=True,
)

# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    try:
        pdf_document = fitz.open(pdf_path)
        pdf_text = ""
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            pdf_text += page.get_text()
        pdf_document.close()
        return pdf_text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

# Function to handle queries
def generate_combined_response(pdf_data, user_input, history):
    # Format the history into a single string
    formatted_history = "\n".join(
        [f"{chat['role'].capitalize()}: {chat['message']}" for chat in history]
    )
    # Format the past data into a single string
    formatted_past_data = "\n".join(
        [f"{chat['role'].capitalize()}: {chat['message']}" for chat in conversation]
    )
    # Construct the prompt to process and summarize the data
    prompt = (
        f"You are a knowledgeable assistant specializing in topics related to Daffodil International University (DIU). "
        f"Your role is to provide accurate, concise, and context-specific responses based on the following inputs:\n\n"
        f"1. **DIU Reference Document**:\n"
        f"The following document contains detailed and official information about DIU, such as policies, courses, events, and guidelines. "
        f"Use this as a key source for your response:\n{pdf_data}\n\n"
        f"2. **Important Past Data**:\n"
        f"Insights and discussions from previous seasons are critical for providing contextually relevant information. "
        f"Here is the relevant data:\n{formatted_past_data}\n\n"
        f"3. **Conversation History**:\n"
        f"Below is the conversation history, which provides additional context about the user's current query and previous discussions:\n{formatted_history}\n\n"
        f"4. **User Query**:\n"
        f"The user has asked the following question or provided this input:\n{user_input}\n\n"
    )
    # Generate and return the response from the UniAssist agent
    response = uniassist_agent.run(prompt)
    return response.content

# Function to handle Email
def handle_email(user_input, history):
    # Format conversation history for context
    formatted_history = "\n".join(
        [f"{chat['role'].capitalize()}: {chat['message']}" for chat in history]
    )
    # Construct a prompt to process and summarize job data
    prompt = (
        f"Draft a professional email based on the following details:\n\n"
        f"Conversation History:\n{formatted_history}\n\n"
        f"User Input (Email Body): {user_input}\n\n"
        f"Make sure to include:\n"
        f"- A relevant subject line\n"
        f"- A polite and professional tone\n"
        f"- Proper email formatting (greetings, body, and closing)\n\n"
        f"Recipient: {RECEIVER_EMAIL}\nSender: {SENDER_NAME}"
    )
    # Generate and return the response from the EmailAgent
    response = email_agent.run(prompt)
    return response.content

# Function to handle Google search queries
def handle_job_search(user_input, history):
    # Format conversation history for context
    formatted_history = "\n".join(
        [f"{chat['role'].capitalize()}: {chat['message']}" for chat in history]
    )
    # Use the WebsiteTools to retrieve job listings from a specified URL
    try:
        knowledge_base = search_agent.tools[0].read_url(
            "https://www.linkedin.com/jobs/search/?currentJobId=4118244113&geoId=103363366&origin=JOB_SEARCH_PAGE_LOCATION_AUTOCOMPLETE&refresh=true"
        )
    except Exception as e:
        return f"Error accessing job search portal: {e}"
    # Construct a prompt to process and summarize job data
    prompt = (
        f"You are a job search assistant specializing in providing structured and concise job search results.\n\n"
        f"Retrieved job portal data (truncated for processing):\n{knowledge_base[:5000]}\n\n"
        f"User Query: {user_input}\n\n"
        f"Context:\n"
        f"The user is searching for jobs relevant to their interests. Summarize the most relevant and recent results.\n\n"
        f"Conversation History:\n{formatted_history}\n\n"
        f"Expected Response Format:\n"
        f"- **Job Title:** [Job Title]\n"
        f"- **Application Deadline:** [Deadline]\n"
        f"- **Key Requirements:** [Requirements]\n\n"
        f"Include actionable insights, links, and concise explanations where applicable."
    )
    # Generate and return the response from the SearchAgent
    response = search_agent.run(prompt)
    return response.content

# Streamlit app UI
def main():
    st.title("UniAssist")
    st.write("Welcome to **UniAssist**! I am here to assist you.")
    # st.markdown(
    #     """
    #     ### Features:
    #     - **University Information**: Learn about DIU policies, courses, and events.
    #     - **Email Assistance**: Get help drafting professional and context-specific emails.
    #     - **Jobs Search**: Find the latest opportunities tailored to your needs.
    #     """
    # )

    # Sidebar button to clear chat history
    with st.sidebar:
        if st.button("Clear Chat History"):
            st.session_state.chat_history.clear()
            save_conversation_history([])
            st.success("Chat history cleared!")

    # Initialize chat history in session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = conversation_history

    # Fixed path to the PDF file (ensure this path is correct)
    pdf_path = "DIU.pdf"
    # Extract text from the fixed PDF
    pdf_data = extract_text_from_pdf(pdf_path)

    if not pdf_data:
        st.error("Failed to extract text from the PDF.")
        return

    # Chat interface using st.chat_input
    user_input = st.chat_input("Ask me anything about DIU...")

    if user_input:
        # Store user input in chat history
        st.session_state.chat_history.append({"role": "user", "message": user_input})
        # Display the user's message
        st.chat_message("user").markdown(user_input)

        if "email" in user_input.lower():
            with st.spinner("Generating your email..."):
                response = handle_email(user_input, st.session_state.chat_history)

        elif "job" in user_input.lower():
            with st.spinner("Searching for updates..."):
                response = handle_job_search(user_input, st.session_state.chat_history)

        else:
            with st.spinner("Processing your question..."):
                response = generate_combined_response(pdf_data, user_input, st.session_state.chat_history)
            
        # Store response in chat history
        st.session_state.chat_history.append({"role": "assistant", "message": response})
        # Display the response message
        st.chat_message("assistant").markdown(f"**Assistant**: {response}")

        # Save updated history
        save_conversation_history(st.session_state.chat_history)

    # Display conversation history
    for chat in st.session_state.chat_history:
        role = "You" if chat["role"] == "user" else "Assistant"
        st.chat_message(chat["role"]).markdown(f"**{role}**: {chat['message']}")

if __name__ == "__main__":
    main()
