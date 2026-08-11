import streamlit as st
import chatbot_backend as demo
import database as db
import auth
import rag

# Line 6 - Page configuration - sets browser tab title and icon
st.set_page_config(page_title="Pratik's Assistant", page_icon="🤖")

# Line 9-115 - CSS styling for entire app - applies to both login page and chatbot page
st.markdown("""
<style>
    /* Sets entire app background to white */
    .stApp { background-color: #ffffff; }
    
    /* Makes all paragraph text black so visible on white background */
    .stMarkdown p { color: black !important; }
    
    /* Makes chat message text black for both user and assistant bubbles */
    [data-testid="stChatMessage"] p { color: black !important; }
    
    /* Makes sidebar text black */
    [data-testid="stSidebar"] p { color: black !important; }
    
    /* Makes sidebar dropdown and label text black */
    [data-testid="stSidebar"] label { color: black !important; }
    
    /* Makes assistant message bubble same grey color as user message bubble */
    [data-testid="stChatMessage"] { background-color: #e6e6e6 !important; }
    
    /* Makes login and register input field labels black */
    .stTextInput label { color: black !important; }
    
    /* Makes all headings black */
    h1, h2, h3 { color: black !important; }
    
    /* Makes caption text black - used for password hint */
    .stCaption { color: black !important; }
    
    /* Makes selectbox label black in sidebar */
    .stSelectbox label { color: black !important; }
    
    /* Makes metric label and value black in sidebar */
    [data-testid="stMetricLabel"] { color: black !important; }
    [data-testid="stMetricValue"] { color: black !important; }
    
    /* Makes tab background white so black text is visible */
    .stTabs [data-baseweb="tab-list"] { background-color: #ffffff !important; }
    
    /* Makes tab text black so readable on white tab background */
    .stTabs [data-baseweb="tab"] { 
        color: black !important; 
        background-color: #ffffff !important;
    }
    
    /* Makes active selected tab slightly grey so user knows which tab is open */
    .stTabs [aria-selected="true"] {
        background-color: #f0f0f0 !important;
        color: black !important;
    }
    
    /* Makes Login and Register button white background with black text */
    .stButton > button {
        background-color: #ffffff !important;
        color: black !important;
        border: 2px solid #cccccc !important;
        border-radius: 8px !important;
    }
    
    /* Makes button slightly grey on hover so user knows its clickable */
    .stButton > button:hover {
        background-color: #f0f0f0 !important;
        color: black !important;
        border: 2px solid #999999 !important;
    }
    
    /* Makes input box background white same as login button */
    .stTextInput input {
        background-color: #ffffff !important;
        color: black !important;
        border: 2px solid #cccccc !important;
        border-radius: 8px !important;
    }
    
    /* Makes input box border change on focus instead of red highlight */
    .stTextInput input:focus {
        background-color: #ffffff !important;
        color: black !important;
        border: 2px solid #999999 !important;
    }
    
    /* Makes error message text black so visible on red background */
    [data-testid="stAlert"] p { color: black !important; }
    
    /* Makes warning message text black so visible on yellow background */
    [data-testid="stAlert"] { color: black !important; }
    
    /* Makes success message text black so visible on green background */
    div[role="alert"] p { color: black !important; }
    div[role="alert"] { color: black !important; }
    
    /* Makes numbered list items text black in chat responses
       Previously list items were merging with grey bubble background */
    [data-testid="stChatMessage"] ol li { color: black !important; }
    
    /* Makes bullet list items text black in chat responses
       Previously bullet points were merging with grey bubble background */
    [data-testid="stChatMessage"] ul li { color: black !important; }
    
    /* Makes bold text black inside chat responses
       Previously bold headings were not visible on grey background */
    [data-testid="stChatMessage"] strong { color: black !important; }
    
    /* Forces ALL text inside chat bubbles to black
       This catches any text color not covered by rules above */
    [data-testid="stChatMessage"] * { color: black !important; }
    
    /* Makes file uploader text black in sidebar */
    .stFileUploader label { color: black !important; }
    
    /* Makes file uploader helper text black */
    .stFileUploader span { color: black !important; }
</style>
""", unsafe_allow_html=True)

# Line 118 - Initialize authentication session state
# logged_in - tracks if user is currently logged in or not
# username - stores the logged in users username for DynamoDB queries
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Line 124 - Initialize username in session state
if 'username' not in st.session_state:
    st.session_state.username = None

# Line 127 - LOGIN / REGISTER PAGE
# This page is shown when user is NOT logged in
# Once logged in this section is skipped and chatbot page is shown
if not st.session_state.logged_in:

    # Line 131 - Title and subtitle for login page
    st.markdown("<h1 style='color: black; text-align: center;'>🤖 Pratik's Chatbot</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: grey;'>Powered by AWS Bedrock + LangChain</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Line 135 - Two tabs - Login and Register
    # User clicks tab to switch between logging in and creating account
    tab1, tab2 = st.tabs(["Login", "Register"])

    # Line 139 - LOGIN TAB
    with tab1:
        st.markdown("### Login to your account")

        # Line 142 - Input fields for username and password
        # type="password" hides the password text with asterisks
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")

        # Line 147 - Login button click handler
        if st.button("Login", key="login_btn"):
            if login_username and login_password:
                # Send credentials to Cognito via auth.py for verification
                result = auth.login_user(login_username, login_password)

                if result == login_username:
                    # Line 153 - Login successful - save username and mark as logged in
                    st.session_state.logged_in = True
                    st.session_state.username = login_username
                    # Refresh page to hide login form and show chatbot
                    st.rerun()
                else:
                    # Line 158 - Login failed - show error returned from Cognito
                    st.error(f"Login failed: {result}")
            else:
                # Line 161 - Show warning if fields are empty
                st.warning("Please enter both username and password")

    # Line 164 - REGISTER TAB
    with tab2:
        st.markdown("### Create a new account")

        # Line 167 - Input fields for new user registration
        reg_username = st.text_input("Username", key="reg_username")
        reg_email = st.text_input("Email", key="reg_email")
        reg_password = st.text_input("Password", type="password", key="reg_password")
        reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")

        # Line 173 - Password requirements hint shown below fields
        st.caption("Password must have 8+ characters, uppercase, lowercase, number and special character (!@#$%^&*)")

        # Line 176 - Register button click handler
        if st.button("Register", key="reg_btn"):
            if reg_username and reg_email and reg_password and reg_confirm:
                if reg_password != reg_confirm:
                    # Line 179 - Passwords dont match - show error before calling Cognito
                    st.error("Passwords do not match")
                else:
                    # Line 182 - Validate password format before sending to AWS
                    password_check = auth.is_valid_password(reg_password)

                    if password_check == True:
                        # Line 185 - Send registration request to Cognito via auth.py
                        result = auth.register_user(reg_username, reg_password, reg_email)

                        if result == True:
                            # Line 188 - Registration successful - tell user to login
                            st.success("Account created successfully! Please login.")
                        else:
                            # Line 191 - Registration failed - show error from Cognito
                            st.error(f"Registration failed: {result}")
                    else:
                        # Line 194 - Password format invalid - show which requirement failed
                        st.error(password_check)
            else:
                # Line 197 - Show warning if any field is empty
                st.warning("Please fill in all fields")

# Line 200 - CHATBOT PAGE
# This section is only shown after successful login
# st.session_state.logged_in must be True to reach here
else:

    # Line 204 - Title shown after login
    st.markdown("<h1 style='color: black;'>Hi, This is Assistant of Pratik 😎</h1>", unsafe_allow_html=True)

    # Line 207 - Initialize LangChain memory once per session
    # Memory stores conversation history for context aware responses
    if 'memory' not in st.session_state:
        st.session_state.memory = demo.demo_memory()

    # Line 212 - Load chat history from DynamoDB for this specific logged in user
    # Each user has separate chat history stored under their username
    if 'chat_history' not in st.session_state:
        # Fetch messages from DynamoDB using logged in username as user_id
        saved_messages = db.get_chat_history(st.session_state.username)

        # Line 217 - Convert DynamoDB format to session state format
        # DynamoDB stores {user_id, timestamp, role, message}
        # Session state needs {role, text}
        st.session_state.chat_history = [
            {"role": msg["role"], "text": msg["message"]}
            for msg in saved_messages
        ]

    # Line 224 - SIDEBAR
    with st.sidebar:
        st.markdown("### 🤖 Pratik's Assistant")
        st.caption("Powered by AWS Bedrock + LangChain")
        st.markdown("---")

        # Line 229 - Show which user is currently logged in
        st.markdown(f"👤 **Logged in as:** {st.session_state.username}")
        st.markdown("---")

        # Line 233 - Response style dropdown - controls how bot responds
        # Selected style is passed to backend prompt template selector
        st.markdown("### 🎨 Response Style")
        style = st.selectbox(
            "Choose how the bot responds:",
            ["Short", "Detailed", "Formal"],
            index=0  # Default is Short
        )
        st.markdown("---")

        # Line 243 - PDF Upload section for RAG
        # User uploads a PDF and all questions are answered from PDF content
        # When no PDF is uploaded chatbot uses normal LLM responses
        st.markdown("### 📄 Upload PDF")
        uploaded_pdf = st.file_uploader(
            "Upload a PDF to chat with it",
            type="pdf",
            key="pdf_uploader"
        )

        # Line 251 - Process PDF when uploaded
        # vector_store stored in session state so it persists across messages
        # pdf_name stored so we detect when a new different PDF is uploaded
        if uploaded_pdf is not None:
            if 'vector_store' not in st.session_state or st.session_state.get('pdf_name') != uploaded_pdf.name:
                with st.spinner("Reading PDF..."):
                    # Process PDF - splits into chunks and creates FAISS vector store
                    st.session_state.vector_store = rag.process_pdf(uploaded_pdf)
                    # Save PDF name to detect when new PDF is uploaded
                    st.session_state.pdf_name = uploaded_pdf.name
                st.success("PDF ready! Ask questions about it.")
        else:
            # Line 262 - Clear vector store when PDF is removed by user
            if 'vector_store' in st.session_state:
                del st.session_state.vector_store
                del st.session_state.pdf_name

        st.markdown("---")

        # Line 268 - Shows total messages in current session
        st.metric("Messages", len(st.session_state.chat_history))
        st.markdown("---")

        # Line 272 - Clear chat - deletes all messages from DynamoDB and session state
        if st.button("🗑️ Clear Chat"):
            db.delete_chat_history(st.session_state.username)
            st.session_state.chat_history = []
            st.session_state.memory = demo.demo_memory()
            st.rerun()

        st.markdown("---")

        # Line 280 - Logout button - clears all session data and goes back to login page
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.chat_history = []
            st.session_state.memory = demo.demo_memory()
            st.rerun()

    # Line 288 - Display all previous messages from chat history
    # Loops through and renders each message with correct avatar
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["text"])

    # Line 294 - Chat input box fixed at bottom of page
    # Returns None when empty returns text string when user presses Enter
    input_text = st.chat_input("Chat with Pratik's Bot here")

    if input_text:
        # Line 298 - Display user message immediately in chat window
        with st.chat_message("user"):
            st.markdown(input_text)

        # Line 302 - Save user message to DynamoDB under logged in username
        db.save_message(st.session_state.username, "user", input_text)

        # Line 305 - Add user message to session state chat history
        st.session_state.chat_history.append({"role": "user", "text": input_text})

        # Line 308 - Get response from backend
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):

                # Line 311 - Check if PDF is uploaded in session state
                # If PDF uploaded answer from PDF content using RAG
                # If no PDF uploaded use normal chatbot with conversation memory
                if 'vector_store' in st.session_state:
                    # Line 315 - PDF is uploaded - answer from PDF using RAG
                    # RAG searches PDF chunks for relevant content then answers
                    chat_response = rag.answer_from_pdf(
                        input_text,
                        st.session_state.vector_store
                    )
                    # Line 320 - Add note so user knows answer came from PDF
                    chat_response = chat_response + "\n\n📄 *Answer from uploaded PDF*"
                else:
                    # Line 323 - No PDF uploaded - use normal chatbot with memory
                    # Passes selected style to use correct prompt template
                    chat_response = demo.demo_conversation(
                        input_text=input_text,
                        memory=st.session_state.memory,
                        style=style
                    )
            st.markdown(chat_response)

        # Line 331 - Save assistant response to DynamoDB under logged in username
        db.save_message(st.session_state.username, "assistant", chat_response)

        # Line 334 - Add assistant response to session state chat history
        st.session_state.chat_history.append({"role": "assistant", "text": chat_response})