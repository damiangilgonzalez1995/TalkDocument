#Import the required Libraries
import streamlit as st
import pandas as pd
from streamlit_extras.let_it_rain import rain

st.set_page_config(layout="wide")

rain(emoji="🎆",animation_length=5)
st.markdown(f"<h1 style='text-align: center; color: black;'> QA Document with LLMs</h1>", unsafe_allow_html=True)
st.markdown(f"<h2 style=' color: black;'> Welcome!! If you want to use this tool you must follow the steps:</h2>", unsafe_allow_html=True)
st.markdown(f"<h3 style=' color: black;'> Step 1️⃣ Create Data Base: Creation of the database from the provided data source</h3>", unsafe_allow_html=True)
st.markdown(f"<h3 style=' color: black;'> Step 2️⃣ Ask to the document: You can now converse with your document with the help of the LLM</h3>", unsafe_allow_html=True)
