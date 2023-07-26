from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
import os

import streamlit as st
import streamlit.components.v1 as components

os.environ["OPENAI_API_KEY"] = "{Your_OpenAI_Key}"

prompt_webapp_template = """
    You are a web app developer using Javascript. 
    Please generate a complete functional javascript app 
    following user requirement "{text}".
    The js file and css file should be combined into one html file which can be directly run on server. 
    If there is no CSS requirement specified, please add a Amazon style css in your response.
    The response should only include the content of html file.
    HTML:

    """
PROMPT_WEBAPP = PromptTemplate(template=prompt_webapp_template,
                               input_variables=["text"])

llm = ChatOpenAI(temperature=0.5)
webapp_chain = LLMChain(llm=llm, prompt=PROMPT_WEBAPP,verbose=True)

init_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Example</title>
    <style>
        h3 {
            color: yellow;
        }
    </style>
</head>
<body>
    <h3>Your APP will be displayed here.</h3>
</body>
</html>

"""
st.set_page_config(layout="wide")

if 'html' not in st.session_state:
    st.session_state.html = init_html


def generate():

    requirement = st.session_state.req
    if requirement != '':
        st.session_state.html = webapp_chain.run(requirement)
        print(st.session_state.html)

col1, col2 = st.columns([0.5, 0.5], gap='medium')

with col1:
    st.write("**What kind of Web App do you want me to create?📝**")
    st.text_area("Requirement: ", key='req')
    st.button("Create!", on_click=generate)
    st.code(st.session_state.html, language="typescript")

with col2:
    
    components.html(st.session_state.html, height=600, scrolling=True) 