from langchain_classic.memory import ConversationSummaryBufferMemory
from langchain_classic.chains import ConversationChain
from langchain_classic.prompts import PromptTemplate
from langchain_aws import ChatBedrockConverse

def demo_chatbot():
    """
    Initializes and returns the AWS Bedrock LLM client
    Uses Meta Llama 3.1 8B model via cross-region inference profile
    Bedrock stays on us-east-1 because Llama 3.1 is only available there
    DynamoDB is on ap-south-1 (Mumbai) separately in database.py
    """
    demo_llm = ChatBedrockConverse(
        credentials_profile_name='default',  # Uses AWS CLI default profile
        model="us.meta.llama3-1-8b-instruct-v1:0",  # Llama 3.1 8B model ID
        region_name="us-east-1",  # Bedrock stays us-east-1 - model not in ap-south-1
        temperature=0.1,          # Low temperature = more focused responses
        max_tokens=300            # Limits response length to keep answers concise
    )
    return demo_llm

def demo_memory():
    """
    Creates and returns a LangChain conversation memory object
    ConversationSummaryBufferMemory keeps recent messages and 
    summarizes older ones when token limit is exceeded
    This prevents the context window from overflowing in long conversations
    """
    memory = ConversationSummaryBufferMemory(
        llm=demo_chatbot(),       # Uses same LLM to generate summaries
        max_token_limit=1000      # Summarizes older messages beyond 1000 tokens
    )
    return memory

# Three different prompt templates for different response styles
# Each template instructs the model to respond differently
PROMPT_STYLES = {
    # Short style - forces 1-2 line answers only
    "Short": """You are a helpful assistant.
Rules:
- Answer in 1-2 lines only
- Be direct and to the point
- No extra explanation

Current conversation:
{history}
User: {input}
Assistant:""",

    # Detailed style - gives thorough complete explanations
    "Detailed": """You are a helpful assistant.
Rules:
- Give a thorough and complete explanation
- Use examples where helpful
- Cover all important points

Current conversation:
{history}
User: {input}
Assistant:""",

    # Formal style - uses professional language and tone
    "Formal": """You are a professional assistant.
Rules:
- Use formal and professional language
- Be polite and structured
- Avoid casual language or slang

Current conversation:
{history}
User: {input}
Assistant:"""
}

def demo_conversation(input_text, memory, style="Short"):
    """
    Main function called by frontend to get a response from the chatbot
    input_text - the message typed by the user
    memory     - the LangChain memory object from session state
    style      - response style selected in sidebar (Short/Detailed/Formal)
    """
    # Select the correct prompt template based on user's style selection
    prompt = PromptTemplate(
        input_variables=["history", "input"],
        template=PROMPT_STYLES[style]
    )
    
    # Create conversation chain combining LLM + memory + selected prompt
    llm_conversation = ConversationChain(
        llm=demo_chatbot(),   # AWS Bedrock LLM
        memory=memory,         # Conversation memory for context
        prompt=prompt,         # Selected prompt style template
        verbose=True           # Prints chain details in terminal for debugging
    )
    
    # Invoke the chain with user input and return only the response text
    chat_reply = llm_conversation.invoke(input_text)
    return chat_reply['response']