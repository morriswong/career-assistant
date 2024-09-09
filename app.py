import os
import json
import requests
import pandas as pd
import validators
from urllib.parse import urlparse

import streamlit as st
import streamlit.components.v1 as components

import groq
from groq import Groq

from traceloop.sdk import Traceloop 
from traceloop.sdk.decorators import workflow

Traceloop.init(
    app_name="career_duck", 
    disable_batch=False, 
    api_key=os.environ.get("TRACELOOP_API_KEY")
)

st.set_page_config(
    page_title="Career Duck",
    page_icon="🐤",
    layout="wide",
    initial_sidebar_state="collapsed",
)

def get_plain_text(url):
    """
        Get plain text from a url object.
    """
    if not validators.url(url):
        raise ValueError("Invalid URL")

    parsed_url = urlparse(url)
    if parsed_url.netloc == 'www.linkedin.com':
        raise ValueError("URL is a LinkedIn URL")

    plain_text_url = 'https://r.jina.ai/{url}'
    r = requests.get(plain_text_url.format(url=url))
    return str(r.content)

@workflow(name="generate_bulletpoints")
def generate(prompt, deployment_name, llm='groq'):
    '''
        LLM API call
    '''
    if llm == 'groq':
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    try:
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
    except groq.APIConnectionError as e:
        print("The server could not be reached")
        print(e.__cause__)  # an underlying Exception, likely raised within httpx.
    except groq.RateLimitError as e:
        print("A 429 status code was received; we should back off a bit.")
    except groq.APIStatusError as e:
        print("Another non-200-range status code was received")
        print(e.status_code)
        print(e.response)

    return response, total_tokens, prompt_tokens, completion_tokens

st.title("Career Duck 🐤")
st.subheader("Build your Resume from Job Descriptions")
with st.expander("Check out these job boards"):
    tab1, tab2, tab3, tab4 = st.tabs(["Data", "Finance", "Marketing", "Developer"])
    with tab1:
        st.markdown('https://remoteok.com/remote-jobs')
        st.markdown('https://aijobs.net/')
        st.markdown('https://outerjoin.us/')
        st.markdown('https://himalayas.app/jobs/api')
    with tab2:
        st.markdown('https://www.efinancialcareers.co.uk/jobs')
    with tab3:
        st.write('Coming soon')
    with tab4:
        st.write('Coming soon')
        
form = st.form(key='my-form')
url = form.text_input('Copy and paste the link of the job description below')
submit = form.form_submit_button('Get bullet points')

if submit:
    tab1, tab2, tab3 = st.tabs(["Analysis", "Resume Bullet Points", "Donate"])
    with tab1:
        if url:
            with st.spinner('Analysing the job descriptions'):
                try:
                    url_str = get_plain_text(url)
                    try:
                        prompt = f"""
                            {url_str}
                            
                            Given the job descriptions above, give the following sections:

                            Summary of the job:

                            The ideal profile:

                            Top 5 Skills:                
                            """
                        response, total_tokens, prompt_tokens, completion_tokens = generate(prompt, 'llama3-70b-8192')
                        st.markdown(response)
                    except Exception as e:
                        st.warning("Apologies but too many people is using it now! Please try again later.")
                except ValueError as e:
                    if str(e) == "URL is a LinkedIn URL":
                        st.warning("LinkedIn is strict on crwaling! Use the actual JD link on the career website dinstead.")
                    else:
                        st.error("Invalid URL")
    with tab2:
        if url:
            with st.spinner('Getting bullet points'):
                try:
                    url_str = get_plain_text(url)
                    try:
                        prompt = f"""
                            {url_str}
                            
                            Given this Job Description above, come up with some strong bullet points to show in a resume. Use the XYZ method from Google to write these bullet points

                            Here are some examples of what make a bullet point great:
                            
                            Marketing manager 
                            Increased page views (X) by 23% (Y) in six months by implementing social media distribution strategies (Z). 
                            Reduced ad spend (X) by 30% (Y) by improving customer targeting (Z).
                            
                            Sales specialist
                            Increased conversions (X) by 28% (Y) after training five new team members (Z). 
                            Launched a new product (X) that led to a 15% profit increase in Q1 (Y) by engaging newsletter subscribers (Z). 
                            
                            Customer service 
                            Reduced errors (X) by 40% (Y) after creating a new Standard Operating Procedure (SOP) document (Z). 
                            Increased customer satisfaction (X) by 18% (Y) by implementing survey feedback (Z).                
                            """
                        response, total_tokens, prompt_tokens, completion_tokens = generate(prompt, 'llama3-70b-8192')

                        tab2.subheader("Resume Bullet points suggestions")
                        st.markdown(response)
                    except Exception as e:
                        st.warning("Apologies but too many people is using it now! Please try again later.")
                except ValueError as e:
                    if str(e) == "URL is a LinkedIn URL":
                        st.warning("LinkedIn is strict on crwaling! Use the actual JD link on the career website dinstead.")
                    else:
                        st.error("Invalid URL")
    with tab3:
        with st.spinner('Thanks! Loading the donation page'):
            components.iframe(
                src="https://buymeacoffee.com/morriswch",
                width=None,
                height=800,
                scrolling=False,
            )
        
hide_streamlit_style = """
                <style>
                div[data-testid="stToolbar"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stDecoration"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                div[data-testid="stStatusWidget"] {
                visibility: hidden;
                height: 0%;
                position: fixed;
                }
                #MainMenu {
                visibility: hidden;
                height: 0%;
                }
                header {
                visibility: hidden;
                height: 0%;
                }
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
