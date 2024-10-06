import streamlit as st

class Sidebar:

    MODEL_OPTIONS = ["gpt-3.5-turbo", "gpt-4"]
    TEMPERATURE_MIN_VALUE = 0.0
    TEMPERATURE_MAX_VALUE = 1.0
    TEMPERATURE_DEFAULT_VALUE = 0.0
    TEMPERATURE_STEP = 0.01

    @staticmethod
    def about():
        about = st.sidebar.expander("🧠 About Robby ")
        sections = [
            "#### Robby is an AI chatbot with a conversational memory, designed to allow users to discuss their data in a more intuitive way. 📄",
            "#### It uses large language models to provide users with natural language interactions about user data content. 🌐",
            "#### Powered by [Langchain](https://github.com/hwchase17/langchain), [OpenAI](https://platform.openai.com/docs/models/gpt-3-5) and [Streamlit](https://github.com/streamlit/streamlit) ⚡",
            "#### Source code: [yvann-hub/Robby-chatbot](https://github.com/yvann-hub/Robby-chatbot)",
        ]
        for section in sections:
            about.write(section)

    @staticmethod
    def reset_chat_button():
        if st.button("Reset chat"):
            st.session_state["reset_chat"] = True
        st.session_state.setdefault("reset_chat", False)

    @staticmethod
    def get_user_id():
        with st.sidebar:
            st.header("User Information")
            st.subheader("Enter your User ID (optional)")
            st.write("예시: user_0, user_1, user_2")

            # Only set the user_id if it's not already in session state
            if "user_id" not in st.session_state or st.session_state["user_id"] is None:
                user_id = st.text_input("User ID:", key="user_id_input")
                if user_id:
                    st.session_state["user_id"] = user_id
                    st.success(f"User ID {user_id} set. Now you will get personalized recommendations!")
                    print("user_id", user_id, type(user_id))
                else:
                    st.info("No User ID provided. You will receive general recommendations.")
            else:
                # If user_id is already set, show it
                st.sidebar.write(f"User ID: {st.session_state['user_id']} (Already set)")
                st.sidebar.write(f"User ID 재입력: 새로고침 해주세요")

    #def model_selector(self):
    #    model = st.selectbox(label="Model", options=self.MODEL_OPTIONS)
    #    st.session_state["model"] = model

    #def temperature_slider(self):
    #    temperature = st.slider(
    #        label="Temperature",
    #        min_value=self.TEMPERATURE_MIN_VALUE,
    #        max_value=self.TEMPERATURE_MAX_VALUE,
    #        value=self.TEMPERATURE_DEFAULT_VALUE,
    #        step=self.TEMPERATURE_STEP,
    #    )
    #    st.session_state["temperature"] = temperature
        
    def show_options(self):
        with st.sidebar.expander("🛠️ 대화 리셋", expanded=False):

            self.reset_chat_button()
            #self.model_selector()
            #self.temperature_slider()
            #st.session_state.setdefault("model", self.MODEL_OPTIONS[0])
            #st.session_state.setdefault("temperature", self.TEMPERATURE_DEFAULT_VALUE)


    @staticmethod
    def get_product_type():
        with st.sidebar:
            st.subheader("어떤 금융상품을 추천받으시겠어요?")

            # radio 레이블 공백 제거
            st.markdown(
                """
                <style>
                .stRadio > label {
                    display: none;
                }
                .stRadio > div {
                    margin-top: -20px;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
        
        # 세션에 product_type 값이 없다면 기본값 설정
            if 'product_type' not in st.session_state:
                st.session_state['product_type'] = '적용안함'  # 기본값 설정

            # radio 버튼으로 사용자의 선택을 받음
            product_type = st.radio(
                '',
                ('적용안함', '예금', '적금', '예금 & 적금'),
                index=('적용안함', '예금', '적금', '예금 & 적금').index(st.session_state['product_type'])  # 기본값 유지
            )

            # 선택한 값을 세션 상태에 저장
            st.session_state['product_type'] = product_type

            st.write(f"선택한 금융상품: {st.session_state['product_type']}")