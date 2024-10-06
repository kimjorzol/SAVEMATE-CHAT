import streamlit as st

class Layout:
    
    def show_header(self, product_names):
        """
        Displays the header of the app
        """
        st.markdown(
            f"""
            <h1 style='text-align: center; color: lightblue;'> Save Mate에게 {product_names} 추천받으세요! 😁</h1>
            """,
            unsafe_allow_html=True,
        )

    def show_api_key_missing(self):
        """
        Displays a message if the user has not entered an API key
        """
        st.markdown(
            """
            <div style='text-align: center;'>
                <h4>Enter your <a href="https://platform.openai.com/account/api-keys" target="_blank">OpenAI API key</a> to start chatting</h4>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def prompt_form(self):
        """
        Displays the prompt form
        """
        with st.form(key="my_form", clear_on_submit=True):
            user_input = st.text_area(
                "Query:",
                placeholder="자유롭게 질문하세요",
                key="input",
                label_visibility="collapsed",
            )
            submit_button = st.form_submit_button(label="Send")

            print("submit_button:",submit_button)
            print('user_input:',user_input)
            
            # true or false가 나와야할 것 같은데 이상함
            is_ready = submit_button #and user_input

        return is_ready, user_input
    
