from sql_chain import execute_queries_with_retries

import os
import streamlit as st
import pandas as pd

from langchain.chains.conversation.memory import ConversationBufferWindowMemory

from groq import Groq
from langchain.chains import ConversationChain, LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

from langchain_experimental.agents import create_pandas_dataframe_agent

from dotenv import load_dotenv

load_dotenv()

llm_model = "llama3-8b-8192"
llm_temperature = 0

api_key = os.environ.get("GROQ_API_KEY")

llm = ChatGroq(model=llm_model, temperature=llm_temperature, api_key=api_key)

# Used this for a single non-memory chain in the sidebar
client = Groq(api_key=api_key)

system = "{system_text}"
human = "{human_text}"
prompt = ChatPromptTemplate.from_messages([("human", human), ("system", system)])
chain = prompt | llm

# Remembers the last 10 messages
conversational_memory_length = 100
memory = ConversationBufferWindowMemory(k=conversational_memory_length, memory_key="chat_history", return_messages=True)

# Title
st.title('An AI Assistant for Data Analysis 🤖')

# Welcoming message
st.write('Hello, I am your AI assistant and I am here to help you with your data analysis tasks.')

# Explanation sidebar
with st.sidebar:
    st.write('*Your Data Analysis Adventure Begins With Your Data.*')

    st.caption('''**You may already know that every exciting data project starts with the data.
               That's why I would love for you to upload your CSV file.**''')
    st.caption('''**Once we have your data in hand, we'll dive into understanding it. Then we'll work together to shape your business challenge into a data analysis framework.
              I'll introduce you to the coolest machine learning models, and we'll use them to tackle your problem.**''')
    st.caption('''**Sounds fun right?**''')

    st.divider()

    st.caption("<p style = 'text-align: center'> Developed by Ray Wienand </p>", unsafe_allow_html=True)

 
# NOTE! Initiated a single call to groq as to NOT add this to the memory chain
# Function sidebar
# @st.cache_data # Looks like the cache is slowing this down
def steps_da():
    chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": "What are the steps of Data Analysis?",
                    }
                ],
                model="llama3-8b-8192",
                temperature=0
            )
    return chat_completion

chat_completion = steps_da()

with st.sidebar:
        with st.expander("What are the steps of Data Analysis?"):         
            st.write(chat_completion.choices[0].message.content)

# Initialise a session state variable
if 'clicked' not in st.session_state:
    st.session_state.clicked = {1: False}

# Function to update the value in session state
def clicked(button):
    st.session_state.clicked[button] = True          

# Button
st.button("Let's get started", on_click=clicked, args=[1])
if st.session_state.clicked[1]: 
    
    my_query = """
    Give me the name of the top 100 customers with the highest purchase frequency, 
    but with under average AOV. 

    Include frequency and aov. Also include the products they bought.
    """
    st.write(my_query)

    response = execute_queries_with_retries(my_query)
    st.write(response)

    # user_csv = st.file_uploader("Upload your file here", type="csv")  

    # if user_csv is not None:
    #     # Ensure pointer is at the start of the file
    #     user_csv.seek(0)
    #     df = pd.read_csv(user_csv, low_memory=False)
        
    #     # Create the pandas agent after df is defined
    #     pandas_agent = create_pandas_dataframe_agent(llm, df, allow_dangerous_code=True, verbose=True)
    #     question = 'What is the meaning of the columns'
    #     columns_meaning = pandas_agent.run(question)
    #     st.write(columns_meaning)

    # Functions of the main script
    @st.cache_data
    def function_agent(response):
        # st.write("**Data Overview**")
        # st.write("The database consists of the following tables:")
        # st.write(response.head())
        # st.write("**Data Cleaning**")
        # columns_df = response("What are the meaning of the tables?")
        # st.write(columns_df)
        # missing_values = response("How many missing sales values does the database have? Start the answer with 'There are'")
        # st.write(missing_values)
        duplicates_query = """
        Are there any duplicate products, and if so where?
        """
        st.write(duplicates_query)
        duplicates = execute_queries_with_retries(duplicates_query)
        st.write(duplicates)
        client_query = """
        Give me an alphabetical list of all clients
        """
        st.write(client_query)
        client_list = execute_queries_with_retries(client_query)
        st.write(client_list)
        # st.write("**Data Summarization**")
        # st.write(response.describe())
        # correlation_analysis = response("Calculate correlations between numerical variables to identify potential relationships.")
        # st.write(correlation_analysis)
        # outliers = response("Identify outliers in the data that may be erroneous or that may have a significant impact on the analysis.")
        # st.write(outliers)
        # new_features = response("What new features would be interesting to create?.")
        # st.write(new_features)

        return function_agent

    # Main
    st.header("Exploratory Data Analysis")
    st.subheader("Response to questions")

    function_agent(response)

    user_question = st.text_input("What would you like to know?")
