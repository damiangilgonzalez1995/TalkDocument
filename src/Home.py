#Import the required Libraries
import streamlit as st
from streamlit_extras.let_it_rain import rain
import os

st.set_page_config(layout="wide", page_icon="👋",)

rain(emoji="🎆",animation_length=5)
st.markdown(f"<h1 style='text-align: center; color: black;'> QA Document with LLMs</h1>", unsafe_allow_html=True)



try:
    hf_key = os.environ['HUGGINGFACE_API_KEY']
except:
    st.markdown("<h2 style='text-align: center;color: orange;'>Environment variable 'HUGGINGFACE_API_KEY' not detected. In order to use the tool you must add your huggingface key.</h2>", unsafe_allow_html=True)
    hf_key = st.text_input("🌕 Please, enter your HUGGINGFACE api key.", type="password")

if hf_key:

    st.session_state["hf_key"] = hf_key

    st.markdown(f"<h2 style=' color: black;'> Welcome!! If you want to use this tool you must follow the steps:</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3 style=' color: black;'> Step 1️⃣ Create Data Base: Creation of the database from the provided data source</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style=' color: black;'> Step 2️⃣ Ask to the document: You can now converse with your document with the help of the LLM</h3>", unsafe_allow_html=True)


left_co, cent_co,last_co = st.columns(3)
with cent_co:
    st.image("resources\img\schema.PNG")

