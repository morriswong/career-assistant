import os
import requests
import json

import streamlit as st
from streamlit_chat import message  

from groq import Groq
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(
    page_title="Career Assitant",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Create the Groq client
client_groq = Groq(api_key=os.environ.get('GROQ_API_KEY'), )

# Set the system prompt
system_prompt = {
    "role": "system",
    "content":
    "You are a helpful assistant. You reply with very short answers."
}

# endregion

# region PROMPT SETUP

default_prompt = """
You are an AI assistant that helps users write concise\
 reports on sources provided according to a user query.\
 You will provide reasoning for your summaries and deductions by\
 describing your thought process. You will highlight any conflicting\
 information between or within sources. Greet the user by asking\
 what they'd like to investigate.
"""

# system_prompt = st.sidebar.text_area("System Prompt", default_prompt, height=200)
seed_message = {"role": "system", "content": default_prompt}
# endregion

# region SESSION MANAGEMENT
# Initialise session state variables
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "messages" not in st.session_state:
    st.session_state["messages"] = [seed_message]
if "model_name" not in st.session_state:
    st.session_state["model_name"] = []
if "cost" not in st.session_state:
    st.session_state["cost"] = []
if "total_tokens" not in st.session_state:
    st.session_state["total_tokens"] = []
if "total_cost" not in st.session_state:
    st.session_state["total_cost"] = 0.0
# endregion

# region SIDEBAR SETUP

counter_placeholder = st.sidebar.empty()
counter_placeholder.write(
    f"Total cost of this conversation: ${st.session_state['total_cost']:.5f}"
)
clear_button = st.sidebar.button("Clear Conversation", key="clear")

if clear_button:
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["messages"] = [seed_message]
    st.session_state["number_tokens"] = []
    st.session_state["model_name"] = []
    st.session_state["cost"] = []
    st.session_state["total_cost"] = 0.0
    st.session_state["total_tokens"] = []
    counter_placeholder.write(
        f"Total cost of this conversation: £{st.session_state['total_cost']:.5f}"
    )


download_conversation_button = st.sidebar.download_button(
    "Download Conversation",
    data=json.dumps(st.session_state["messages"]),
    file_name=f"conversation.json",
    mime="text/json",
)

def get_plain_text(url):
    """
    Get plain text from a url object.
    """
    plain_text_url = 'https://r.jina.ai/{url}'
    r = requests.get(plain_text_url.format(url=url))
    return str(r.content)

def generate(prompt, deployment_name, llm='groq'):
    if llm == 'groq':
        client = Groq(api_key='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')
        
    completion = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
        max_tokens=3000
    )
    completion_json = json.loads(completion.to_json())
    response = completion_json['choices'][0]['message']['content']
    total_tokens = completion.usage.total_tokens
    prompt_tokens = completion.usage.prompt_tokens
    completion_tokens = completion.usage.completion_tokens
    return response, total_tokens, prompt_tokens, completion_tokens

st.title("Career Assitant")
col1, col2, col3 = st.columns(3)
with col1:
    col1.subheader("Summarized JD")
    url = st.chat_input(placeholder="The URL of the job description")
    url_str = get_plain_text(url)
    prompt = f"Give me a summary of this role: {url_str}"
    response, total_tokens, prompt_tokens, completion_tokens = generate(url_str, 'llama3-70b-8192')
    st.markdown(url)
    st.markdown(response)
with col2:
    col2.subheader("Must haves and good to haves")
    if url:
        url_str = get_plain_text(url)
        prompt = f"What are the must have and good to have for this role: {url_str}"
        response, total_tokens, prompt_tokens, completion_tokens = generate(prompt, 'llama3-70b-8192')
        st.markdown(response)
with col3:
    col3.subheader("Resume Bullet points suggestions")
    if url:
        url_str = get_plain_text(url)
        prompt = f"""
            {url_str}
            
            Given this JD above, come up with some strong bullet points to show in a resume.
            Here are some examples of what make a bullet point great:
            OK: "Member of Leadership for Tomorrow Society"
            Better: "Selected as one of 275 for this 12-month professional development program for high-achieving diverse talent."
            Best: "Selected as one of 275 participants nationwide for this 12-month professional development program for high-achieving diverse talent based on leadership potential and academic success."
        """
        response, total_tokens, prompt_tokens, completion_tokens = generate(prompt, 'llama3-70b-8192')
        st.markdown(response)
    else:
        st.write("Please enter a prompt")