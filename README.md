# Local-Memory-Chatbot

# MindMate AI – Smart Chatbot with Conversation Memory

## Project Overview

MindMate AI is an intelligent chatbot built using Python, Streamlit, LangChain, and Large Language Models (LLMs). It provides interactive conversations and remembers previous messages using different memory techniques.

The application supports both Ollama for local AI model execution and Groq API for cloud-based AI responses.

# Demo Chatbot Link
https://local-memory-chatbot-qrljvzk8mps43uzhdmvccu.streamlit.app/

## Features

- Interactive AI chatbot with a user-friendly interface.
- Three types of conversation memory.
- **Buffer Memory:** Stores the complete conversation history.
- **Summary Memory:** Creates a summary of previous conversations.
- **Window Memory:** Remembers only the latest three conversation exchanges.
- Supports multiple AI models.
- View stored conversation memory.
- Clear current chat and clear all memories.
- Custom dark-themed Streamlit interface.
- Supports local execution and cloud deployment.

## Technologies Used

- Python
- Streamlit
- LangChain
- LangChain Classic
- LangChain Ollama
- LangChain Groq
- Ollama
- Groq API
- Large Language Models (LLMs)

## Project Structure

```text
MindMate-AI/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── .streamlit/
    └── secrets.toml
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the Project Folder

```bash
cd MindMate-AI
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Key

Create a `.streamlit/secrets.toml` file and add your Groq API key:

```toml
GROQ_API_KEY = "your_api_key"
```

Never upload your API key to GitHub.

### 5. Run the Application

```bash
streamlit run app.py
```

## Memory Types

| Memory Type | Description |
|---|---|
| Buffer Memory | Stores the complete conversation history. |
| Summary Memory | Maintains a summary of previous conversations. |
| Window Memory | Stores the latest three conversation exchanges. |

## Deployment

MindMate AI can be deployed using Streamlit Community Cloud.

1. Upload the project files to GitHub.
2. Open Streamlit Community Cloud.
3. Connect your GitHub repository.
4. Select `app.py` as the main application file.
5. Add `GROQ_API_KEY` under the application's Secrets settings.
6. Deploy the application.

For cloud deployment, select Groq as the AI provider. Ollama running on localhost is intended for local execution.

## Application Usage

1. Open the MindMate AI application.
2. Select an AI provider and model.
3. Choose a conversation memory type.
4. Enter your question in the chat input.
5. View the AI-generated response.
6. Explore stored conversation history using View Memory Contents.

## Future Enhancements

- Persistent conversation storage.
- Chat export functionality.
- Additional AI model support.
- Improved conversation management.


This project is developed for educational and learning purposes.
