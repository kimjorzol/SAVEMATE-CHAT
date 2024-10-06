import os
import streamlit as st
from io import StringIO
import re
import sys
from modules.history import ChatHistory
from modules.layout import Layout
from modules.utils import Utilities
from modules.sidebar import Sidebar
# 추가
#from modules.chatbot import Chatbot
from langchain_core.messages import HumanMessage, AIMessage

#To be able to update the changes made to modules in localhost (press r)
def reload_module(module_name):
    import importlib
    import sys
    if module_name in sys.modules:
        importlib.reload(sys.modules[module_name])
    return sys.modules[module_name]

history_module = reload_module('modules.history')
layout_module = reload_module('modules.layout')
utils_module = reload_module('modules.utils')
sidebar_module = reload_module('modules.sidebar')

ChatHistory = history_module.ChatHistory
Layout = layout_module.Layout
Utilities = utils_module.Utilities
Sidebar = sidebar_module.Sidebar

st.set_page_config(layout="wide", page_icon="💬", page_title="금융상품 추천해주는 | Save Mate")

# Instantiate the main components
layout, sidebar, utils = Layout(), Sidebar(), Utilities()

layout.show_header("금융상품을")

# Get User ID from sidebar before proceeding
Sidebar.get_user_id()

# Get product_type from sidebar before proceeding
Sidebar.get_product_type()

user_api_key = "up_sE1q34hltAbAjZoAj0rfCmVIHh6Ws" #utils.load_api_key()

if not user_api_key:
    layout.show_api_key_missing()
else:
    os.environ["OPENAI_API_KEY"] = user_api_key

    #uploaded_file = utils.handle_upload(["pdf", "txt", "csv"])

    # 종료 등 할 때 사용하기
    chat_flag = True

    if chat_flag:

        # Configure the sidebar
        sidebar.show_options()
        #sidebar.about()

        # Initialize chat history
        history = ChatHistory()
        try:
            print('try to set up chatbot')

            # input parameter 삭제
            #chatbot = utils.setup_chatbot( # setup_chatbot 해야 st.session_state['ready'] = True
                # uploaded_file, st.session_state["model"], st.session_state["temperature"]
            #    uploaded_file, 'model','temp'
            #)
            chatbot = utils.setup_chatbot()
            st.session_state["chatbot"] = chatbot

            if st.session_state["ready"]:
                # Create containers for chat responses and user prompts
                response_container, prompt_container = st.container(), st.container()

                print("1")

                with prompt_container:

                    # Display the prompt form
                    is_ready, user_input = layout.prompt_form()

                    # Initialize the chat history
                    # uploaded_file 없어도 되는지 확인
                    history.initialize("uploaded_file")

                    # Reset the chat history if button clicked
                    # 채팅 리셋하는 기능 만들기
                    #st.session_state["reset_chat"] = False
                    
                    if st.session_state["reset_chat"]:
                        history.reset("uploaded_file")
                        print('Reset')

                    print('it is ready;', is_ready)



                    if is_ready == True:
                
                        print('if is_ready')
                        # Update the chat history and display the chat messages
                        user_id = st.session_state.get("user_id", None)
                        st.write(f"Debug: user_id from session state: {user_id}")
                        print(f"Debug: user_id from session state: {user_id}")
                        if not user_id: # 유저 아이디가 없다면 
                             st.warning("No User ID provided. Continuing in Guest Mode.")
                        history.append("user", user_input)

                        product_type = st.session_state.get("product_type", '적용안함')
                        st.write(f"Debug: product_type from session state: {product_type}")
                        print(f"Debug: product_type from session state: {product_type}")
                        if product_type == '적용안함' : # 상품 적용 안했다면
                             st.warning("금융상품 종류가 입력되지 않았습니다. 기본 채팅모드로 진행합니다")

                        #print('history append')

                        #old_stdout = sys.stdout

                        #print(old_stdout)

                        #sys.stdout = captured_output = StringIO()

                        #print(sys.stdout)



                        print('before output')
                        
                        #output = st.session_state["chatbot"].conversational_chat(user_input)
                        question = user_input
                        query = f"{question.lower()}"
                        context = st.session_state["chatbot"].retrieve_documents(query)

                        # chat_history 가져오기
                        chat_history = st.session_state.get("history", [])

                        output = st.session_state["chatbot"].generate_responses(question, context, st.session_state["history"], user_id=user_id, product_type=product_type) # session_state['history']

                        # 질문과 답변을 저장한다
                        #st.session_state["history"].append((query, output))
                        #st.session_state["history"].append((HumanMessage(query), AIMessage(output)))
                        st.session_state["history"] += [HumanMessage(query), AIMessage(output)]

                        print('after output')

                        #sys.stdout = old_stdout

                        history.append("assistant", output)

                        # Clean up the agent's thoughts to remove unwanted characters
                        #thoughts = captured_output.getvalue()
                        #cleaned_thoughts = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', thoughts)
                        #cleaned_thoughts = re.sub(r'\[1m>', '', cleaned_thoughts)

                        # Display the agent's thoughts
                        #with st.expander("Display the agent's thoughts"):
                        #    st.write(cleaned_thoughts)

                history.generate_messages(response_container)
        except Exception as e:
            st.error(f"Error: {str(e)}")