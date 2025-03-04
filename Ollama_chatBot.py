import streamlit as st
from openai import OpenAIError
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from langchain_community.llms import Ollama

prompt = ChatPromptTemplate.from_messages(
    [('system', 'you are a helpful assistant. Please response to the user quearies'),
     ('user', '{queation}')
     ]
)


def generate_response(queation, llm, temperature, max_tokes):
    try:
        llm = Ollama(model=llm,temperature=temperature)
        output_parser = StrOutputParser()
        chain = prompt | llm | output_parser
        ans = chain.invoke({'queation': queation})
        return ans
    except Exception as e:
        # st.error(f'api error{e}')
        return "❌ Error: Invalid Entry. Please try after sometime."





st.title('Enhanced Q&A Chatbot with Ollama')
st.sidebar.title('Settings')

llm = st.sidebar.selectbox('select the Ollama Model',['gemma2:2b','llama3.2:1b'] )

temperature = st.sidebar.slider('Temperature', min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider('Max Tokens', min_value=50, max_value=300, value=150)
st.subheader('Kindly enter API and Select the model')

st.write('Go ahead and ask any queation')
user_input = st.text_input('enter your queary')
if st.button("Generate Response"):
    if not user_input:
       st.warning("⚠️ Please enter a query.")
    else:
        response = generate_response(user_input, llm, temperature, max_tokens)
        st.write("AI Response:", response)
