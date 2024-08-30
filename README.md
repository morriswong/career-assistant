# Career Assistant

A career-focused chatbot built with Streamlit and Groq

**Overview**

The Career Assitant is a chatbot designed to help users create concise reports on job descriptions, highlighting must-haves and good-to-haves for a particular role. The bot uses natural language processing (NLP) to generate summary bullet points for a resume.

**Features**

1. Summary Generation: Provide a job description URL and the bot will generate a summary of the role.
2. Must-Haves and Good-To-Haves: Enter a job description URL and the bot will provide must-haves and good-to-haves for the role.
3. Resume Bullet Point Suggestions: Enter a job description URL and the bot will suggest strong bullet points for a resume.

**Getting Started**

1. Clone the repository: `git clone <repository_url>`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`
4. Open the app in your browser: `http://localhost:8501`

**System Requirements**

1. Python 3.8+
2. Streamlit 1.12+
3. Groq API Key

**Code Structure**

The code is organized into the following files and directories:

* `app.py`: The main app file, where you can configure the app settings.
* `groq`: The Groq client library.
* `streamlit`: The Streamlit library for building the UI.
* `README.md`: This file.

**Troubleshooting**

If you encounter any issues, refer to the [Streamlit documentation](https://docs.streamlit.io/) and [Groq documentation](https://docs.groq.com/) for troubleshooting tips.

**Contributing**

Contributions are welcome! If you'd like to contribute to the Career Assiant, please fork the repository and create a pull request.

**License**

The Career Assitant is licensed under the Apache License 2.0.