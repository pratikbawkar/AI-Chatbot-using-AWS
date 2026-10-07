# AI Chatbot using AWS Bedrock, LangChain & Streamlit

An AI-powered conversational chatbot built using **AWS Bedrock, LangChain, and Streamlit**. The project supports conversational memory, configurable response styles, user authentication, persistent chat history, and PDF-based question answering using RAG.



## Features

- AI chatbot powered by **Meta Llama 3.1 8B Instruct** on AWS Bedrock
- Conversational memory using LangChain
- Three response styles:
  - Short
  - Detailed
  - Formal
- Streamlit-based web interface
- User authentication using **AWS Cognito**
- Persistent chat history using **Amazon DynamoDB**
- PDF upload and question answering using **RAG**
- Amazon Titan Embeddings with **FAISS** vector search
- Clear chat and logout functionality


## Tech Stack
- **AWS Bedrock** – LLM inference
- **Meta Llama 3.1 8B Instruct** – AI model
- **LangChain** – LLM orchestration, memory and prompt management
- **Streamlit** – Frontend
- **AWS Cognito** – Authentication
- **Amazon DynamoDB** – Chat history
- **FAISS** – Vector store for RAG
- **Amazon Titan Embeddings** – Document embeddings
- **Python / Boto3** – Application and AWS integration
- **PyPDF** – PDF processing

## Architecture


                         User
                           │
                           ▼
                    ┌─────────────┐
                    │  Streamlit  │
                    │  Frontend   │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  LangChain  │
                    │   Backend   │
                    └──────┬──────┘
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
        ┌──────────────┐      ┌──────────────┐
        │ AWS Bedrock  │      │  PDF / RAG   │
        │ Llama 3.1 8B │      │ FAISS Search │
        └──────────────┘      └──────┬───────┘
                                     │
                                     ▼
                                AWS Bedrock

        AWS Cognito ──► User Authentication
        DynamoDB    ──► Persistent Chat History

## Project Structure

```text

ChatBot/
│
├── chatbot_frontend.py
├── chatbot_backend.py
├── auth.py
├── database.py
├── rag.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── docs/
│   ├── architecture.png
│   ├── project-workflow.md
│   └── setup-guide.md
│
└── screenshots/
    ├── login.png
    ├── chatbot.png
    └── pdf-rag.png

```

## File Description



File	Purpose

```text

chatbot_frontend.py         Streamlit UI, authentication flow and chat interface
chatbot_backend.py          Bedrock LLM, LangChain memory, prompts and conversation chain
auth.py                     AWS Cognito registration and login
database.py                 DynamoDB chat history operations
rag.py                      PDF processing, embeddings, FAISS and RAG
requirements.txt	         Python dependencies
```



## How It Works:

```text

Normal Chat

User Input
    ↓
Streamlit
    ↓
LangChain ConversationChain
    ↓
Conversation Memory + Prompt
    ↓
AWS Bedrock
    ↓
Llama 3.1 8B
    ↓
Response
    ↓
Streamlit

```
## PDF Question Answering:

```text


PDF Upload
    ↓
PyPDF
    ↓
Text Extraction
    ↓
Text Chunking
    ↓
Titan Embeddings
    ↓
FAISS Vector Store
    ↓
Relevant Document Chunks
    ↓
AWS Bedrock
    ↓
Answer
```

## Setup

```text

Prerequisites:

Python 3.9+
Anaconda
AWS account
AWS CLI
VS Code
AWS Bedrock model access
AWS Cognito configuration
DynamoDB chat_history table
Install Dependencies
pip install -r requirements.txt
Configure AWS CLI
aws configure



Verify AWS CLI access:

aws s3 ls

The application uses the AWS CLI profile for authentication.

Run the Application

Run:

streamlit run chatbot_frontend.py

Then open:

http://localhost:8501

```




## Security:

```text

Never commit sensitive credentials to GitHub.

Do not upload:

AWS Access Keys
AWS Secret Access Keys
Cognito Client Secrets
.env files
Private keys

Use AWS CLI profiles, environment variables, or AWS Secrets Manager for sensitive configuration.

Disclaimer: For security reasons, all AWS credentials, API keys, passwords, Cognito secrets, and other sensitive authentication details have been removed from the source code before publishing this repository. Therefore, the uploaded source code will not run as-is without configuring your own AWS resources and credentials. Please use your own keys and configuration when running the project.

Example .gitignore:

.env
*.pem
.aws/
__pycache__/
Screenshots

```
Screenshots of the application are available in the screenshots/ directory.

Documentation

Detailed project documentation, architecture diagrams, workflow explanations, and setup information are available in the docs/ directory.

```text

## Future Enhancements
Deploy the application to AWS
Add streaming responses
Add CloudWatch monitoring
Support multiple PDF documents
Persist vector stores
Add conversation export
Add voice input/output
Add multilingual support
Author
```



## Pratik Bawkar

##   AWS | Cloud & DevOps | AI/LLM Applications

