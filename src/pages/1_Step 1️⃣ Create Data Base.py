import streamlit as st
from utils.util import *
import pandas as pd
from streamlit_extras.stylable_container import *
from streamlit_extras.switch_page_button import switch_page
from qa_tool import TalkDocument
from PyPDF2 import PdfReader
from style import *


from streamlit_autorefresh import st_autorefresh

# Define a function to create the "Create Data Base" page
def create_db_page():

    # Define a function to capture user settings
    def __settings_columns():
        openai_key = ""
        # Define the layout for the settings form
        col1, col2  = st.columns(2)
        with col1:
            split_type = st.selectbox("Split type:", SPLIT_TYPE_LIST)
            repo_id = st.text_input("Repo ID", value=REPO_ID_DEFAULT)

        with col2:
            embedding_type = st.selectbox("Embedding type", EMBEDDING_TYPE_LIST, )
            vectorstore_type = st.selectbox("Model VectoreStore Type:", VECTORSTORE_TYPE_LIST)

        if embedding_type == "OPENAI":
            openai_key = st.text_input(label="Please enter your openAI key:")

        return {"split_type": split_type,
                "embedding_type": embedding_type,
                "vectorstore_type" : vectorstore_type,
                "repo_id": repo_id,
                "openai_key": openai_key}
    

    # Set Streamlit page configuration
    st.set_page_config(layout="wide", page_title="Create DB")

    # Initialize user settings in session state
    if "settings" not in st.session_state:
        st.session_state["settings"] = {"split_type": SPLIT_TYPE_LIST[0],
                                        "embedding_type": EMBEDDING_TYPE_LIST[0],
                                        "vectorstore_type" : VECTORSTORE_TYPE_LIST[0],
                                        "repo_id": REPO_ID_DEFAULT}

    st.markdown("<h1 style='text-align: center'>Create Data Base</h1>", unsafe_allow_html=True)

    # Check if Hugging Face API key is provided
    if "hf_key" not in st.session_state:
        st.markdown("<h1 style='text-align: center; color:red'>🌕 Please, enter your HUGGINGFACE api key.</h1>", unsafe_allow_html=True)

    else:
        hf_key = st.session_state["hf_key"]

        document = ""
        url_input = ""
        m = st.markdown(radio_button_style, unsafe_allow_html=True)


        # Create tabs for different sections of the page
        tab_main, tab_settings = st.tabs(["📚 :blue[Documentation]", "✔️ :green[Settings]"])

        # Content for the "Documentation" tab
        with tab_main:
            col_doc, col_pic1 = st.columns(2)

            with col_pic1:
            
                st.markdown("<h1 style='text-align: center'>We support this formats:</h1>", unsafe_allow_html=True)

                st.image("resources\img\Documents.PNG")

            with col_doc:
        
            
                st.markdown("<h1 style='text-align: center; color: black;'>Select the data source</h1>", unsafe_allow_html=True)
        
                # Allow users to select document type (FILE or WEB)
                document_type = st.radio("Type:", ["FILE", "WEB" ], horizontal=True)

                if document_type == "WEB":
                    url_input = st.text_input("Insert URL:")
                    # Aquí podrías implementar la lógica para trabajar con la URL

                elif document_type == "FILE":
                    document = st.file_uploader(f"Sube un archivo {document_type}", type=["txt", "pdf"])

                st.markdown("****")

                if document or url_input:
                    disabled=False
                else:
                    st.markdown(":red[It is necessary to add a document or url] ")
                    disabled=True

                #  Button to create the database
                st.markdown(button_style, unsafe_allow_html=True)
                create_db_button = st.button(" 🚀 CREATE DATA BASE 🚀 ",disabled=disabled)


                if create_db_button:
                    st.session_state["hf_key"]
                    # Determine document type and create TalkDocument object

                    if url_input:
                        talkdocument_object = TalkDocument(data_source_path=url_input,HF_API_TOKEN=hf_key)
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
                        
                        talkdocument_object = TalkDocument(data_text=document_text,HF_API_TOKEN=hf_key)

                    # Get user settings
                    settings_data = st.session_state["settings"]

                    try:
                        # Create the vector storage instance (database)
                        db = talkdocument_object.create_db_document(data_source_type=type_doc,
                                                                    split_type=settings_data["split_type"],
                                                                    embedding_type=settings_data["embedding_type"],
                                                                    vectorstore_type=settings_data["vectorstore_type"],
                                                                    OPENAI_KEY=settings_data["openai_key"])
                        
                        st.session_state["db"] = db
                        st.session_state["object_talkdocument"] = talkdocument_object
                        switch_page("Step 2️⃣ Ask to the document")

                    except Exception as error: 
                        message = f"Error in creation data base: {error}"
                    
                        st.markdown(f"<h2 style='text-align: center; color: red;'>{message}</h2>", unsafe_allow_html=True)


                    

                st.markdown("****")

                if document_type and (url_input or document):


                    container3 = stylable_container(
                    key="container_with_border2",
                    css_styles=container_style)

                    # Display a container with a summary of settings and document information
                    with container3:
                        st.markdown("<h1 style='text-align: center; color: black;'>Configuration Summary</h1>", unsafe_allow_html=True)
                
                        
                        settings_data = st.session_state["settings"]

                        df = pd.DataFrame({
                            "Settings": ["Split type", "Embedding type", "Model VectoreStore Type","Repo ID"] ,
                            "Values": [settings_data["split_type"],
                                        settings_data["embedding_type"],
                                        settings_data["vectorstore_type"],
                                        settings_data["repo_id"]]
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
                st.markdown("<h1 style='text-align: center'>Setting the LLM App </h1>", unsafe_allow_html=True)

                st.image("resources\img\Application.PNG")


            with col_setting:
                st.markdown("<h1 style='text-align: center; color: black;'>Select Settings</h1>", unsafe_allow_html=True)
            

                st.markdown('**Select the settings**:')
                # Desplegables de lista1 y lista2
                


                # REFRESH VALUES IN SESSION_STATE AND PAGE
                settings_values = __settings_columns()

                if st.session_state["settings"] != settings_values:
                    st.session_state["settings"] = {"split_type": settings_values["split_type"],
                                                    "embedding_type": settings_values["embedding_type"],
                                                    "vectorstore_type" : settings_values["vectorstore_type"],
                                                    "repo_id": settings_values["repo_id"],
                                                    "openai_key": settings_values["openai_key"]}
                    st_autorefresh(interval=1000, limit =2)

            
# Run the Streamlit app
if __name__ == "__main__":
    create_db_page()