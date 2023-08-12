import streamlit as st
from utils import *
import pandas as pd
from streamlit_extras.stoggle import stoggle
from streamlit_extras.stylable_container import *
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.let_it_rain import rain
from qa_tool import TalkDocument
from PyPDF2 import PdfReader




# def __init_session():
#         """
#         Initialize the session state for generated queries and past user inputs.
#         """

#         if "generated" not in st.session_state:
#                 st.session_state["in"] = []
            
#         if "past" not in st.session_state:
#             st.session_state["past"] = []


# Página principal
def create_db_page():

    # __init_session

    # st.set_page_config(layout="wide")

    # st.session_state[''] = "NO"

    # st.sidebar.header("Plotting Demo")

    st.title("Create DB")
    document = ""
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
    



    st.markdown("<h1 style='text-align: center; color: black;'>Select the data source</h1>", unsafe_allow_html=True)
    

    container1 = stylable_container(
    key="container_with_border",
    css_styles=style_container,)
    with container1:

        document_type = st.radio("Type:", ["WEB", "FILE"], horizontal=True)

        if document_type == "WEB":
            url_input = st.text_input("Insert URL:",value="https://streamlit.io")
            # Aquí podrías implementar la lógica para trabajar con la URL

        elif document_type == "FILE":
            document = st.file_uploader(f"Sube un archivo {document_type}", type=["txt", "pdf"])
            print(document)
  

    st.markdown("****")
    st.markdown("<h1 style='text-align: center; color: black;'>Select Settings</h1>", unsafe_allow_html=True)
    container2 = stylable_container(
    key="container_with_border2",
    css_styles=style_container,)

    with container2:
        st.markdown('**Select the settings**:')
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

    if document or url_input:
        disabled=False
    else:
        st.markdown(":red[It is necessary to add a document or url] ")
        disabled=True


    want_to_contribute = st.button("🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥 Create DB 🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥🔥",disabled=disabled)
    if want_to_contribute:
        HF_API_TOKEN =  "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"

        if url_input:
            talkdocument_object = TalkDocument(data_source_path=url_input,HF_API_TOKEN=HF_API_TOKEN)

        elif document:

            if document.type == 'text/plain':
                document_text = document.getvalue().decode('utf-8')

            elif document.type == 'application/pdf':
                pdf_readed = PdfReader(document)
                document_text = ""
                for page in pdf_readed.pages:
                    document_text+= page.extract_text()

            talkdocument_object = TalkDocument(data_text=document_text,HF_API_TOKEN=HF_API_TOKEN)

        print(talkdocument_object)
        db = talkdocument_object.create_db_document(data_source_type=document_type,
                                                    split_type=split_type,
                                                    embedding_type=embedding_type,
                                                    vectorstore_type=vectorstore_type)
        
        print(db)
        st.session_state["db"] = db

        
        switch_page("consult")

    st.markdown("****")

    if document_type and (url_input or document):

        st.markdown("<h1 style='text-align: center; color: black;'>Configuration Summary</h1>", unsafe_allow_html=True)

        st.markdown("""<style>table {
                      {style_container}
                }
                </style>
                """, unsafe_allow_html=True)

        df = pd.DataFrame({
            "Settings": [split_type, embedding_type, vectorstore_type, repo_id],
            "Values": ["Split type", "Embedding type", "VectoreStore Type","Repo ID"]

        })

        st.markdown("**You are going to create a database with the following settings:**")

        container3 = stylable_container(
        key="container_with_border2",
        css_styles=style_container,)

        with container3:

            st.markdown("****")
            st.markdown(f"**Document Source Type: {document_type}**")
            stoggle(
                "Document Info",
                f"""{document}{url_input}""",
            )

            st.markdown("****")
            st.table(df)
            







    # if opcion and (url_input or document):
    #     if st.button("Va a ser creada la base de datos"):
    #         st.session_state['APTO'] = "APTO"






    # with col1:
    #     st.button("📆", on_click=style_button_row, kwargs={
    #         'clicked_button_ix': 1, 'n_buttons': 4
    #     })
    # with col2:
    #     st.button("👌", on_click=style_button_row, kwargs={
    #         'clicked_button_ix': 2, 'n_buttons': 4
    #     })
    # with col3:
    #     st.button("◀", on_click=style_button_row, kwargs={
    #     'clicked_button_ix': 3, 'n_buttons': 4

    #     })
    # with col4:
    #     st.button("🚧", on_click=style_button_row, kwargs={
    #         'clicked_button_ix': 4, 'n_buttons': 4
    #     })
        



    
create_db_page()