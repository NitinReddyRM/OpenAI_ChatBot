import streamlit as st
from openai import OpenAIError
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages(
    [('system', 'you are a helpful assistant. Please response to the user quearies'),
     ('user', '{queation}')
     ]
)


def generate_response(queation, api_key, llm, temperature, max_tokes):
    # api_key = api_key
    try:
        llm = ChatOpenAI(model=llm,api_key=api_key)
        output_parser = StrOutputParser()
        chain = prompt | llm | output_parser
        ans = chain.invoke({'queation': queation})
        return ans
    except Exception as e:
        # st.error(f'api error{e}')
        return "❌ Error: Invalid API key. Please enter a valid API key."
    except OpenAIError as e:
        # st.error(f'api error{e}')
        return f"⚠️ An unexpected error occurred: {str(e)}"





st.title('Enhanced Q&A Chatbot with OpenAI')
st.sidebar.title('Settings')
api_key = st.sidebar.text_input('Enter your open AI API Key*', type='password')

llm = st.sidebar.selectbox('Select an open AI Model*', ['gpt-4o', 'gpt-4-turbo', 'gpt-4'])


temperature = st.sidebar.slider('Temperature', min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider('Max Tokens', min_value=50, max_value=300, value=150)
st.subheader('Kindly enter API and Select the model')

st.write('Go ahead and ask any queation')
user_input = st.text_input('enter your queary')
if st.button("Generate Response"):
    if not api_key:
        st.warning("⚠️ Please enter a valid OpenAI API key.")
    elif not user_input:
       st.warning("⚠️ Please enter a query.")
    else:
        response = generate_response(user_input, api_key, llm, temperature, max_tokens)
        st.write("AI Response:", response)
