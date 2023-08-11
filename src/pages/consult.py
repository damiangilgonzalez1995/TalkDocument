import streamlit as st

def consultas_page():
    st.title("Consultas")
    APTO = st.session_state['APTO']
    st.text(APTO)

consultas_page()