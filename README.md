# UniAssist  AI Agent Documentation

## Overview
UniAssist is an AI-powered virtual assistant designed to help users with:
- Answering queries related to Daffodil International University (DIU)
- Drafting and sending emails
- Searching for current job circulars through different websites

It leverages AI models and various tools to deliver relevant and structured information efficiently.

## Features
1. **University Information Query Handling**
   - Provides detailed responses about DIU policies, courses, and events.
   - Uses a PDF document containing DIU-related information for reference.
   
2. **Email Assistance**
   - Generates professional, context-specific emails.
   - Supports email formatting including subject line, greetings, body, and closing.
   - Requires user confirmation before sending emails.
   
3. **Job Search Assistance**
   - Searches for relevant job listings using Google Search and WebsiteTools.
   - Extracts key job details, including title, application deadline, and requirements.
   - Formats job information in a structured manner for easy readability.

## Technologies Used
- **Programming Language**: Python
- **Framework**: Streamlit
- **AI Model**: Groq (Llama 3.3-70b-versatile)
- **Libraries & Tools**:
  - `phi.agent` (AI agent management)
  - `phi.model.groq` (AI model integration)
  - `phi.tools.email` (Email generation and sending)
  - `phi.tools.googlesearch` (Web search integration)
  - `phi.tools.website` (Extracting website information)
  - `PyMuPDF (fitz)` (PDF text extraction)
  - `json` (Conversation history management)
  - `dotenv` (Environment variable management)

## Setup & Configuration
1. **Environment Variables**
   - Ensure the following environment variables are set:
     ```
     SENDER_EMAIL=<your-email>
     SENDER_NAME=<your-name>
     SENDER_PASSKEY=<email-passkey>
     RECEIVER_EMAIL=<recipient-email>
     ```

2. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```sh
   streamlit run UniAssist.py
   ```

## Functionality Breakdown
### 1. Query Handling
- Loads DIU-related content from a reference PDF.
- Uses historical conversations to maintain context.
- Processes user queries and generates responses.

### 2. Email Drafting
- Extracts key details from user input.
- Formats the email professionally.
- Requires confirmation before sending.

### 3. Job Search
- Uses web scraping tools to extract job listings.
- Structures search results for clarity.
- Retrieves only the most relevant listings.

## User Interaction Flow
1. **User enters a query in the chat interface**.
2. **UniAssist processes the query and provides a response**.
3. If the query relates to email drafting, **it generates a draft and seeks confirmation**.
4. If the query is about job search, **it retrieves job listings and presents structured data**.
5. **Conversation history is saved for better context awareness**.

## Future Improvements
- Expand integration with more university-related resources.
- Enhance job search accuracy using dedicated APIs.
- Improve email customization and scheduling features.

## Conclusion
UniAssist is a powerful AI agent designed to assist students, faculty, and job seekers by providing instant information, drafting professional emails, and fetching job opportunities efficiently. The system ensures structured responses and an easy-to-use interface for enhanced user experience.

