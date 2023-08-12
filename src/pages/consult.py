import streamlit as st

def consultas_page():
    st.title("Consultas")
    db = st.session_state['db']
    print("RRR", db)

consultas_page()