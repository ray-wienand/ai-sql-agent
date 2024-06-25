from sql_chain import execute_queries_with_retries

import os
import streamlit as st


# Main
st.title('An AI Assistant for Data Analysis 🤖')
st.write('Hello, I am your AI assistant and I am here to help you with your data analysis tasks.')

with st.sidebar:
    st.write('*Your Data Analysis Adventure Begins with your data.*')

    st.caption('''**You may already know that every exciting data project starts with the data.
               That's why I would love for you to upload your CSV file.**''')
    st.caption('''**Once we have your data in hand, we'll dive into understanding it. Then we'll work together to shape your business challenge into a data analysis framework.
              I'll introduce you to the coolest machine learning models, and we'll use them to tackle your problem.**''')   
    st.caption('''**Sounds fun right?**''')

    st.divider()

    st.caption("<p style = 'text-align: center'> Developed by Ray Wienand </p>", unsafe_allow_html=True)


my_query = """
Give me the name of the top 100 customers with highest purchase frequency 
#     but with under average AOV. 

#     Include frequency and aov.
"""

result = execute_queries_with_retries(my_query)
print(result)