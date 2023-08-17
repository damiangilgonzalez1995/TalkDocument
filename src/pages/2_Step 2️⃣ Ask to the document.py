import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from streamlit_extras.let_it_rain import rain
from style import *



# Define a function to create the "Query" page
def query_page():
    # Set Streamlit page configuration
    st.set_page_config(layout="wide", page_title="Talk Document")

    # Define columns for layout
    col_ask, col_pic3 = st.columns(2)

    # Content for the right column (col_pic3)
    with col_pic3:
        st.markdown("<h1 style='text-align: center'>How it works</h1>", unsafe_allow_html=True)

        st.image("docs\img\Query.PNG")

    # Content for the left column (col_ask)
    with col_ask:

        st.markdown("<h1 style='text-align: center'>Chat with the document</h1>", unsafe_allow_html=True)

        if not 'db' in st.session_state:
            st.markdown("<h3 style='text-align: center ; color: red;'>You must create a Data Base</h3>", unsafe_allow_html=True)
            rain(emoji="⚠️")

            # Display button and allow switching to the previous step
            st.markdown(button_step2, unsafe_allow_html=True)
            go_back = st.button("Go to the previous step")
            if go_back:
                switch_page("Step 1️⃣ Create Data Base")

           
        else:
            db = st.session_state['db']
            # Initialize session state variables for user input and responses
            if "generated" not in st.session_state:
                    st.session_state["generated"] = []
                
            if "past" not in st.session_state:
                st.session_state["past"] = []

            # Get user input
            user_input = st.text_input(label=f"Question",
                                    value="Talk me about the document")


            
            if st.button("ASK"):
                    object_talkdocument = st.session_state["object_talkdocument"]
                    response = object_talkdocument.do_question(user_input, repo_id=st.session_state["settings"]["repo_id"])
                    st.session_state.past.append(user_input)
                    st.session_state.generated.append(response)

            if st.session_state["generated"]:
        
                    for i in range(len(st.session_state["generated"])-1, -1, -1):
    

                        question = st.session_state["past"][i]
   

                        st.markdown(f"<h3 style='text-align: center; color: black;'> ........................................................................</h3>", unsafe_allow_html=True)
                        
                        st.markdown(f"<h4 style='text-align: center; color: black;'> Question:</h4>", unsafe_allow_html=True)
                        st.markdown(f"<h4 style=' color: red;'>  {question}</h4>", unsafe_allow_html=True)
                        chat_message = st.session_state["generated"][i]["output_text"]
                        st.markdown(f"<h4 style='text-align: center; color: black;'> Anwser:</h4>", unsafe_allow_html=True)
                        st.markdown(f"<h4 style=' color: green;'>  {chat_message}</h4>", unsafe_allow_html=True)


                
                        
       


# Run the Streamlit app
if __name__ == "__main__":
    consultas_page()