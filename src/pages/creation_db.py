import streamlit as st
from utils import *
import pandas as pd

print(DS_TYPE_LIST)

# Lista de opciones para los desplegables
DS_TYPE_LIST = ["Opción 1", "Opción 2", "Opción 3"]
lista2 = ["Opción A", "Opción B", "Opción C"]


def color_survived(val):
    return 'background-color: #ACE5EE'

# Página principal
def create_db_page():
    st.session_state['APTO'] = "NO"

    st.sidebar.header("Plotting Demo")

    st.title("Create DB")
    archivo = ""
    url_input = ""

    # Selección de tipo de entrada (URL, PDF, TXT)
    opcion = st.radio("Que tipo de archivo vas a introducir", ("URL", "PDF", "TXT"), horizontal=True)

    if opcion == "URL":
        url_input = st.text_input("Ingresa la URL:")
        # Aquí podrías implementar la lógica para trabajar con la URL

    elif opcion in ("PDF", "TXT"):
        archivo = st.file_uploader(f"Sube un archivo {opcion}", type=[opcion.lower()])
        if archivo is not None:
            # Aquí podrías implementar la lógica para trabajar con el archivo
            print("error")

    # Desplegables de lista1 y lista2
    col1, col2  = st.columns(2)



    with col1:
        split_type = st.selectbox("Split type:", SPLIT_TYPE_LIST)
    with col2:
        embedding_type = st.selectbox("Embedding type", EMBEDDING_TYPE_LIST)

    col3, col4  = st.columns(2)
    with col3:
        vectorstore_type = st.selectbox("VectoreStore Type:", VECTORSTORE_TYPE_LIST)
    with col4:
        repo_id = st.text_input("Repo ID", value=REPO_ID_DEFAULT)

    st.text("You are going to create a database with this config:")

    df = pd.DataFrame({
        "Split type": [split_type],
        "Embedding type": [embedding_type],
        "VectoreStore Type": [vectorstore_type],
        "Repo ID": [repo_id]

    })
    st.dataframe(df.style.applymap(color_survived))




    if opcion in ("URL", "PDF", "TXT") and (url_input or archivo):
        if st.button("Va a ser creada la base de datos"):
            st.session_state['APTO'] = "APTO"

    st.text("HELLOOO")
    

    
create_db_page()