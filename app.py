import requests
import json

import streamlit as st
from streamlit_chat import message  

from groq import Groq
from dotenv import load_dotenv
load_dotenv()

from traceloop.sdk import Traceloop 
from traceloop.sdk.decorators import workflow

Traceloop.init(
    app_name="career_duck", 
    disable_batch=False, 
    api_key=st.secrets['TRACELOOP_API_KEY']
)


st.set_page_config(
    page_title="Career Duck",
    page_icon="🦆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

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

def get_plain_text(url):
    """
        Get plain text from a url object.
    """
    plain_text_url = 'https://r.jina.ai/{url}'
    r = requests.get(plain_text_url.format(url=url))
    return str(r.content)

@workflow(name="generate_bulletpoints")
def generate(prompt, deployment_name, llm='groq'):
    '''
        LLM api call
    '''
    if llm == 'groq':
        client = Groq(api_key=st.secrets['GROQ_API_KEY'])
        
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

st.title("Career Duck 🦆")
st.subheader("Turn Job Descriptions to Resume Bullet Points")
form = st.form(key='my-form')
url = form.text_input('Enter the link of the job description')
submit = form.form_submit_button('Get bullet points')

if submit:        
    col1, col2, col3 = st.columns(3)
    with col1:
        if url:
            with st.spinner('Getting summary'):
                url_str = get_plain_text(url)
                prompt = f"Give me a brief summary of this role: {url_str}"
                response, total_tokens, prompt_tokens, completion_tokens = generate(url_str, 'llama3-70b-8192')
                col1.subheader("Summary")
                st.markdown(response)
        with col2:
            with st.spinner('Getting must haves and good to haves '):
                if url:
                    url_str = get_plain_text(url)
                    prompt = f"What are the must have and good to have for this role: {url_str}"
                    response, total_tokens, prompt_tokens, completion_tokens = generate(prompt, 'llama3-70b-8192')
                    col2.subheader("Must haves and good to haves")
                    st.markdown(response)
        with col3:
            with st.spinner('Getting bullet points'):
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
                    col3.subheader("Resume Bullet points suggestions")
                    st.markdown(response)