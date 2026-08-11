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

```text
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