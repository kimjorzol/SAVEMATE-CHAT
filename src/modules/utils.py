import os
import pandas as pd
import streamlit as st
import pdfplumber
from langchain_chroma import Chroma
#from langchain_community.vectorstores import Chroma
from modules.chatbot import Chatbot
from modules.embedder import Embedder

from dotenv import load_dotenv

class Utilities:

    @staticmethod
    def load_api_key():
        # API 키 로드 순서
        ## 우선 .env 파일에서 API 키가 설정되어 있는지 확인 -> 이 서비스는 사용자에게 직접 키를 받는 형식이므로 .env에 없을 것
        ## .env 퍄앨에서 찾지 못할 경우 세션 상태에 저장된 API 키를 확인하여 가져옴
        ## 세션에도 없을 경우 사용자에게 다시 키를 입력하도록 요청 & 입력받은 키를 세션에 저장
        """
        Loads the OpenAI API key from the .env file or 
        from the user's input and returns it
        """
        if not hasattr(st.session_state, "api_key"):
            st.session_state.api_key = None
            print('os.path:', os.path)
        
        # key 가져오기
        load_dotenv()
        user_api_key = 'up_sE1q34hltAbAjZoAj0rfCmVIHh6Ws' #os.getenv("UPSTAGE_API_KEY")


        #you can define your API key in .env directly
        #if os.path.exists(".env") and os.environ.get("OPENAI_API_KEY") is not None:
        #    print("os.path.exist 확인")
            # user_api_key = os.environ["OPENAI_API_KEY"]
        #    user_api_key = 'up_sE1q34hltAbAjZoAj0rfCmVIHh6Ws'
        #    st.sidebar.success("API key loaded from .env", icon="🚀")
        #else:
            
            #if st.session_state.api_key is not None:
            #    user_api_key = st.session_state.api_key
                #st.sidebar.success("API key loaded from previous input", icon="🚀")
            #else:
            #    user_api_key = st.sidebar.text_input(
            #        label="#### Your OpenAI API key 👇", placeholder="sk-...", type="password"
            #    )
            #    if user_api_key:
            #        st.session_state.api_key = user_api_key
        
        # 임시로
        #user_api_key = 'up_sE1q34hltAbAjZoAj0rfCmVIHh6Ws'

        return user_api_key

    
    @staticmethod
    def handle_upload(file_types):
        """
        Handles and display uploaded_file
        :param file_types: List of accepted file types, e.g., ["csv", "pdf", "txt"]
        """

        print("handle_upload")

        uploaded_file = st.sidebar.file_uploader("upload", type=file_types, label_visibility="collapsed")
        if uploaded_file is not None:

            def show_csv_file(uploaded_file):
                file_container = st.expander("Your CSV file :")
                uploaded_file.seek(0)
                shows = pd.read_csv(uploaded_file)
                file_container.write(shows)

            def show_pdf_file(uploaded_file):
                file_container = st.expander("Your PDF file :")
                with pdfplumber.open(uploaded_file) as pdf:
                    pdf_text = ""
                    for page in pdf.pages:
                        pdf_text += page.extract_text() + "\n\n"
                file_container.write(pdf_text)
            
            def show_txt_file(uploaded_file):
                file_container = st.expander("Your TXT file:")
                uploaded_file.seek(0)
                content = uploaded_file.read().decode("utf-8")
                file_container.write(content)
            
            def get_file_extension(uploaded_file):
                return os.path.splitext(uploaded_file)[1].lower()
            
            file_extension = get_file_extension(uploaded_file.name)

            # Show the contents of the file based on its extension
            #if file_extension == ".csv" :
            #    show_csv_file(uploaded_file)
            if file_extension== ".pdf" : 
                show_pdf_file(uploaded_file)
            elif file_extension== ".txt" : 
                show_txt_file(uploaded_file)

        else:
            st.session_state["reset_chat"] = True

        print(uploaded_file.name)
        
        return uploaded_file

    @staticmethod
    def setup_chatbot(): #(uploaded_file, model, temperature):
        """
        Sets up the chatbot with the uploaded file, model, and temperature
        """
        embeds = Embedder()

        #with st.spinner("Processing..."):
        #    uploaded_file.seek(0)
        #    file = uploaded_file.read()
        #    print(uploaded_file.name)
            # Get the document embeddings for the uploaded file
            #vectors = embeds.getDocEmbeds(file, uploaded_file.name)
        #vectors = 'vectors' # 안씀

            # Create a Chatbot instance with the specified model and temperature
            
            # 추가
        #    embedding_function = embeds.#get_embedding_function()
        #    vector_store = Chroma(
        #        persist_directory='/Users/sohi/Downloads/trial1_1/embeddings',
        #        embedding_function=embedding_function
        #    )

        #    retriever = vector_store.as_retriever()

        #    print('Go to Chatbot __init__')
        #    chatbot = Chatbot('model', 'temperature', #vector_store, retriever)
        #    print('Chatbot __init__ ??')

        ####
        #uploaded_file.seek(0)
            #file = uploaded_file.read()
        #print(uploaded_file.name)
            # Get the document embeddings for the uploaded file
            #vectors = embeds.getDocEmbeds(file, uploaded_file.name)
        #vectors = 'vectors' # 안씀

            # Create a Chatbot instance with the specified model and temperature
            
            # 추가
        
        
        ## embedding function ~~ 등 모두 Embedder 단에서 처리하도록 한다.
        ## model 등 여러번 설정하게 되어버림.
        #embedding_function = embeds.get_embedding_function()
        #vector_store = Chroma(
        #    persist_directory='/Users/sohi/Downloads/trial1_1/embeddings',
        #    embedding_function=embedding_function
        #)

        #retriever = vector_store.as_retriever()

        # Embedder.py 에서 해결해야 함
        retriever = embeds.get_retriever()

        print('Go to Chatbot __init__')

        # retriever만 
        chatbot = Chatbot(retriever)
        #print('Chatbot __init__ ??')


        ###
        
        st.session_state["ready"] = True

        print(st.session_state['ready'])

        return chatbot
