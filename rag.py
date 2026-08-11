import boto3
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import RetrievalQA
from langchain_aws import ChatBedrockConverse
import tempfile
import os

# Initialize AWS Bedrock client for embeddings
# Embeddings convert text into numbers so we can search for similar content
bedrock_client = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'  # Bedrock stays us-east-1
)

def get_embeddings():
    """
    Creates embeddings model using AWS Bedrock
    Embeddings convert text chunks into numbers (vectors)
    Similar text gets similar numbers so we can find relevant chunks
    Uses Amazon Titan Embeddings model which is cheap and available
    """
    embeddings = BedrockEmbeddings(
        client=bedrock_client,
        model_id="amazon.titan-embed-text-v1"  # Free tier eligible embedding model
    )
    return embeddings

def process_pdf(uploaded_file):
    """
    Takes an uploaded PDF file from Streamlit
    Splits it into chunks and creates a searchable vector store
    uploaded_file - the file object from st.file_uploader
    Returns a FAISS vector store that can be searched
    """
    # Save uploaded file temporarily to disk so PyPDFLoader can read it
    # Streamlit uploads are in memory so we need to save them first
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    # Load PDF and extract text from all pages
    loader = PyPDFLoader(tmp_path)
    documents = loader.load()

    # Split text into smaller chunks for better search results
    # chunk_size=1000 means each chunk is about 1000 characters
    # chunk_overlap=200 means chunks overlap by 200 chars to avoid missing context
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_documents(documents)

    # Create vector store from chunks using Bedrock embeddings
    # FAISS is a local vector database - no extra cost
    embeddings = get_embeddings()
    vector_store = FAISS.from_documents(chunks, embeddings)

    # Delete temporary file after processing
    os.unlink(tmp_path)

    return vector_store

def answer_from_pdf(question, vector_store):
    """
    Answers a question using content from the uploaded PDF
    question     - the user's question text
    vector_store - the FAISS vector store created from the PDF
    Returns answer string based on PDF content
    """
    # Initialize the same LLM used by chatbot
    llm = ChatBedrockConverse(
        credentials_profile_name='default',
        model="us.meta.llama3-1-8b-instruct-v1:0",
        region_name="us-east-1",
        temperature=0.1,
        max_tokens=500
    )

    # Create retrieval chain that searches PDF and answers questions
    # RetrievalQA searches vector store for relevant chunks then asks LLM
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",  # stuff = put all retrieved chunks into prompt
        retriever=vector_store.as_retriever(
            search_kwargs={"k": 3}  # retrieve top 3 most relevant chunks
        )
    )

    # Get answer from PDF content
    result = qa_chain.invoke({"query": question})
    return result["result"]