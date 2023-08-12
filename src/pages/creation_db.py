import streamlit as st
from utils import *
import pandas as pd
from st_aggrid import AgGrid
from streamlit_extras.stoggle import stoggle
from streamlit_extras.stylable_container import *




print(DS_TYPE_LIST)

# Lista de opciones para los desplegables



def color_survived(val):
    return 'background-color: #ACE5EE'

# Página principal
def create_db_page():

    # st.set_page_config(layout="wide")

    st.session_state['APTO'] = "NO"

    st.sidebar.header("Plotting Demo")

    st.title("Create DB")
    archivo = ""
    url_input = ""
  
    

 
    st.markdown("""
    <style>
    .stRadio [role=radiogroup]{
        align-items: center;
        justify-content: center;
        
    }
    </style>
    """,unsafe_allow_html=True)

    style_container = """{
            border: 1px solid rgba(49, 51, 63, 0.2);
            border-radius: 0.5rem;
            padding: calc(1em - 1px);
            background: rgb(122,226,159);
            background: linear-gradient(90deg, rgba(122,226,159,0.7730741954985119) 32%, rgba(219,128,211,1) 63%, rgba(0,212,255,1) 100%);
        }
        """



    container1 = stylable_container(
    key="container_with_border",
    css_styles=style_container,)
    
    container2 = stylable_container(
    key="container_with_border2",
    css_styles=style_container,)

    container3 = stylable_container(
    key="container_with_border2",
    css_styles=style_container,)

    with container1:

        st.markdown('**Select the document**:')
        opcion = st.radio("Type:", DS_TYPE_LIST, horizontal=True)

        if opcion == "WEB":
            url_input = st.text_input("Insert URL:",value="https://streamlit.io")
            # Aquí podrías implementar la lógica para trabajar con la URL

        elif opcion in ("PDF", "FILE"):
            archivo = st.file_uploader(f"Sube un archivo {opcion}", type=[opcion.lower()])
            if archivo is not None:
                # Aquí podrías implementar la lógica para trabajar con el archivo
                print("error")


    with container2:
        st.markdown('**Select the configuration**:')
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

    st.markdown("****")


    

    st.markdown("""
<style>
table {
                      
{style_container}
                }
                

</style>
""", unsafe_allow_html=True)
    
    

    df = pd.DataFrame({
        "Configuration": [split_type, embedding_type, vectorstore_type, repo_id],
        "Characteristics": ["Split type", "Embedding type", "VectoreStore Type","Repo ID"]

    }).set_index("Characteristics")

    with container3:

        st.markdown("**You are going to create a database with this config:**")

        # AgGrid(df)
        st.table(df)
        st.markdown(f"**Document Source Type: {opcion}**")
        # st.table(df.style.applymap(color_survived))
        stoggle(
            "Document Source Type",
            f"""{opcion}""",
        )







    if opcion in ("URL", "PDF", "TXT") and (url_input or archivo):
        if st.button("Va a ser creada la base de datos"):
            st.session_state['APTO'] = "APTO"

    advanced = st.expander("EXPAND", expanded = False)
    with advanced:
        st.text("HELLOOO")



    
create_db_page()