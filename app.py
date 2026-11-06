import os
import streamlit as st

from langchain_groq import ChatGroq
from langchain_classic.memory import (
    ConversationBufferMemory,
    ConversationSummaryMemory,
    ConversationBufferWindowMemory
)
from langchain_core.prompts import ChatPromptTemplate


# ---------------- PAGE SETTINGS ----------------

st.set_page_config(
    page_title="MindMate AI",
    page_icon="💬",
    layout="wide"
)


# ---------------- LIGHT THEME ----------------

st.markdown("""
<style>
.stApp {
    background-color: #F5F6F8;
    color: #222222;
}

.main-title {
    color: #222222 !important;
    text-align: center;
    font-size: 38px;
    font-weight: bold;
}

.subtitle {
    color: #555555 !important;
    text-align: center;
    font-size: 16px;
}

section[data-testid="stSidebar"] {
    background-color: #E9EAED;
}

section[data-testid="stSidebar"] * {
    color: #222222 !important;
}

.stApp p, .stApp label, .stApp h1,
.stApp h2, .stApp h3, .stApp li {
    color: #222222 !important;
}

[data-testid="stChatMessage"] {
    background-color: #FFFFFF !important;
    border: 1px solid #DDDDDD;
    border-radius: 12px;
    padding: 14px;
}

[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li {
    color: #222222 !important;
}

[data-testid="stChatInput"] {
    background-color: #FFFFFF !important;
}

[data-testid="stChatInput"] textarea {
    color: #222222 !important;
    -webkit-text-fill-color: #222222 !important;
    background-color: #FFFFFF !important;
    caret-color: #222222 !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #777777 !important;
    -webkit-text-fill-color: #777777 !important;
}

[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background-color: #FFFFFF;
    color: #222222;
}

.stButton button {
    background-color: #E2E4E8;
    color: #222222 !important;
    border: 1px solid #CCCCCC;
    border-radius: 8px;
}

[data-testid="stExpander"] {
    background-color: #FFFFFF;
    border: 1px solid #DDDDDD;
}
</style>
""", unsafe_allow_html=True)


# ---------------- API KEY ----------------

def get_api_key():
    key = os.environ.get("GROQ_API_KEY")

    if not key:
        try:
            key = st.secrets.get("GROQ_API_KEY", "")
        except Exception:
            key = ""

    return key.strip() if key else ""


api_key = get_api_key()


# ---------------- MODEL SETTINGS ----------------

MODEL_OPTIONS = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant"
]


def load_llm(model_name):
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Add it in Streamlit Cloud Secrets."
        )

    return ChatGroq(
        model=model_name,
        temperature=0.3,
        api_key=api_key
    )


# ---------------- MEMORY SETTINGS ----------------

def create_memory(memory_type, llm):

    if memory_type == "Buffer Memory":
        return ConversationBufferMemory(
            memory_key="history",
            input_key="input",
            output_key="output",
            return_messages=False
        )

    elif memory_type == "Summary Memory":
        return ConversationSummaryMemory(
            llm=llm,
            memory_key="history",
            input_key="input",
            output_key="output",
            return_messages=False
        )

    else:
        return ConversationBufferWindowMemory(
            k=3,
            memory_key="history",
            input_key="input",
            output_key="output",
            return_messages=False
        )


# ---------------- SESSION STATE ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "memories" not in st.session_state:
    st.session_state.memories = {}


# ---------------- SIDEBAR ----------------

st.sidebar.title("Settings")

provider = "Groq"
st.sidebar.text("Provider: Groq")

model_name = st.sidebar.selectbox(
    "Choose Model",
    MODEL_OPTIONS
)

memory_type = st.sidebar.selectbox(
    "Choose Memory Type",
    [
        "Buffer Memory",
        "Summary Memory",
        "Window Memory"
    ]
)

st.sidebar.markdown("---")

st.sidebar.write("**Active Memory:**", memory_type)
st.sidebar.write("**Provider:**", provider)
st.sidebar.write("**Model:**", model_name)

if st.sidebar.button("Clear Current Chat"):
    st.session_state.messages = []
    st.rerun()

if st.sidebar.button("Clear All Memories"):
    st.session_state.memories = {}
    st.session_state.messages = []
    st.rerun()


# ---------------- INITIALIZE MODEL AND MEMORY ----------------

memory_id = f"{model_name}_{memory_type}"

try:
    llm = load_llm(model_name)

    if memory_id not in st.session_state.memories:
        st.session_state.memories[memory_id] = create_memory(
            memory_type, llm
        )

    memory = st.session_state.memories[memory_id]

except Exception as error:
    st.error(f"Model initialization failed: {error}")
    st.info(
        "Add your GROQ_API_KEY in Streamlit Cloud Settings → Secrets."
    )
    st.stop()


# ---------------- RESPONSE GENERATION ----------------

def generate_response(user_input):

    history = memory.load_memory_variables({})["history"]

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are MindMate AI, a friendly and helpful chatbot. "
            "Use the conversation history to remember relevant details. "
            "Answer clearly and naturally.\n\n"
            "Conversation history:\n{history}"
        ),
        ("human", "{input}")
    ])

    formatted_prompt = prompt.format_messages(
        history=history,
        input=user_input
    )

    response = llm.invoke(formatted_prompt)
    answer = response.content

    memory.save_context(
        {"input": user_input},
        {"output": answer}
    )

    return answer


# ---------------- MAIN CHAT INTERFACE ----------------

st.markdown(
    '<div class="main-title">MindMate AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Your AI chatbot with conversational memory</div>',
    unsafe_allow_html=True
)

st.write("")

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer = generate_response(user_input)
                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as error:
                st.error(f"Error generating response: {error}")


# ---------------- VIEW MEMORY ----------------

st.markdown("---")

with st.expander("View Memory Contents"):

    memory_content = memory.load_memory_variables({})

    st.write("**Current Memory Type:**", memory_type)

    st.write("**Stored Conversation:**")

    if memory_content.get("history"):
        st.text(memory_content["history"])
    else:
        st.info("No conversation has been stored yet.")
