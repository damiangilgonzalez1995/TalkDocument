import streamlit as st
from utils import *
import pandas as pd
from streamlit_extras.stoggle import stoggle
from streamlit_extras.stylable_container import *
from streamlit_extras.switch_page_button import switch_page
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

from streamlit_autorefresh import st_autorefresh

# Página principal
def create_db_page():

    st.set_page_config(layout="wide", page_title="Create DB")

    if "settings" not in st.session_state:
        st.session_state["settings"] = {"split_type": SPLIT_TYPE_LIST[0],
                                        "embedding_type": EMBEDDING_TYPE_LIST[0],
                                        "vectorstore_type" : VECTORSTORE_TYPE_LIST[0],
                                        "repo_id": REPO_ID_DEFAULT}

    st.markdown("<h1 style='text-align: center'>Create Data Base</h1>", unsafe_allow_html=True)

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

    






    tab_main, tab_settings = st.tabs(["📚 :blue[Documentation]", "✔️ :green[Settings]"])

    

    with tab_main:
        col_doc, col_pic1 = st.columns(2)

        with col_pic1:
        
            st.markdown("<h1 style='text-align: center'>QA Document Schema</h1>", unsafe_allow_html=True)

            st.image("docs\img\youarehere1.PNG")

        with col_doc:
    
        
            st.markdown("<h1 style='text-align: center; color: black;'>Select the data source</h1>", unsafe_allow_html=True)
       

            document_type = st.radio("Type:", ["FILE", "WEB" ], horizontal=True)

            if document_type == "WEB":
                url_input = st.text_input("Insert URL:")
                # Aquí podrías implementar la lógica para trabajar con la URL

            elif document_type == "FILE":
                document = st.file_uploader(f"Sube un archivo {document_type}", type=["txt", "pdf"])


            if document or url_input:
                disabled=False
            else:
                st.markdown(":red[It is necessary to add a document or url] ")
                disabled=True

            st.markdown("****")
            m = st.markdown("""<style>
                                div.stButton > button:first-child {
                                    font-weight: bolder;
                                    background: rgb(222,181,151);
                                    background: linear-gradient(90deg, rgba(222,181,151,1) 0%, rgba(223,232,200,1) 94%););
                                }</style>""", unsafe_allow_html=True)
            
            create_db_button = st.button("🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖 CREATE DATA BASE 🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖🤖",disabled=disabled)


            if create_db_button:
                HF_API_TOKEN =  "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"

                if url_input:
                    talkdocument_object = TalkDocument(data_source_path=url_input,HF_API_TOKEN=HF_API_TOKEN)
                    type_doc = "WEB"

                elif document:

                    if document.type == 'text/plain':
                        document_text = document.getvalue().decode('utf-8')
                        type_doc = "PDF"

                    elif document.type == 'application/pdf':
                        pdf_readed = PdfReader(document)
                        document_text = ""
                        
                        for page in pdf_readed.pages:
                            document_text+= page.extract_text()
                            type_doc = "TXT"
                    
                    talkdocument_object = TalkDocument(data_text=document_text,HF_API_TOKEN=HF_API_TOKEN)

                settings_data = st.session_state["settings"]

                print(settings_data)
                
                db = talkdocument_object.create_db_document(data_source_type=type_doc,
                                                            split_type=settings_data["split_type"],
                                                            embedding_type=settings_data["embedding_type"],
                                                            vectorstore_type=settings_data["vectorstore_type"])
                
                st.session_state["db"] = db
                st.session_state["object_talkdocument"] = talkdocument_object
                switch_page("2º)ask to the document")

            st.markdown("****")

            if document_type and (url_input or document):


                container3 = stylable_container(
                key="container_with_border2",
                css_styles="""{border: 3px solid black;
                                background: rgb(222,181,151);
                                background: linear-gradient(90deg, rgba(222,181,151,1) 0%, rgba(223,232,200,1) 94%);}""")

                
                with container3:
                    st.markdown("<h1 style='text-align: center; color: black;'>Configuration Summary</h1>", unsafe_allow_html=True)
            
                    
                    settings_data = st.session_state["settings"]

                    df = pd.DataFrame({
                        "Settings": ["Split type", "Embedding type", "VectoreStore Type","Repo ID"] ,
                        "Values": [settings_data["split_type"], settings_data["embedding_type"],settings_data["vectorstore_type"],settings_data["repo_id"]]
                    })

                    st.markdown("**You are going to create a database with the following settings:**")

                    st.markdown(f"**Document Source Type: {document_type}**")
                    if document:
                        st.markdown(f"**Document Source Name: {document.name}**")
                    elif url_input:
                        st.markdown(f"**URL: {url_input}**")


                    st.markdown("****")
                    st.table(df)


    with tab_settings:

        col_setting, col_pic2 = st.columns(2)

        with col_pic2:
            st.markdown("<h1 style='text-align: center'>QA Document Schema</h1>", unsafe_allow_html=True)

            st.image("docs\img\youarehere2.PNG")


        with col_setting:
            st.markdown("<h1 style='text-align: center; color: black;'>Select Settings</h1>", unsafe_allow_html=True)
           

            st.markdown('**Select the settings**:')
            # Desplegables de lista1 y lista2
            col1, col2  = st.columns(2)
            with col1:
                split_type = st.selectbox("Split type:", SPLIT_TYPE_LIST)
            with col2:
                embedding_type = st.selectbox("Embedding type", EMBEDDING_TYPE_LIST, )

            col3, col4  = st.columns(2)
            with col3:
                vectorstore_type = st.selectbox("VectoreStore Type:", VECTORSTORE_TYPE_LIST)
            with col4:
                repo_id = st.text_input("Repo ID", value=REPO_ID_DEFAULT)


            # REFRESH VALUES IN SESSION_STATE AND PAGE
            settings_values = {"split_type": split_type,
                                "embedding_type": embedding_type,
                                "vectorstore_type" : vectorstore_type,
                                "repo_id": repo_id}

            if st.session_state["settings"] != settings_values:
                st.session_state["settings"] = {"split_type": split_type,
                                                "embedding_type": embedding_type,
                                                "vectorstore_type" : vectorstore_type,
                                                "repo_id": repo_id}
                st_autorefresh(interval=1000, limit =2)

        
        
        

# def compare_values(dict_values, split_type):

#     if dict_values["split_type"] != split_type:
#         count = st_autorefresh(interval=1000, limit =1)
#         print("refresh",count)



        

  



    
            















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