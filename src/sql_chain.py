import os
# import pickle
import re
import sqlite3
import pandas as pd

# Langchain imports
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.memory import ChatMessageHistory

# Schema imports
from schema import extract_db_schema
from get_schema import get_schema

# from groq import Groq

from dotenv import load_dotenv

load_dotenv()

# Custom Exception
class BadRequestError(Exception):
    """Custom exception for handling bad requests."""
    pass

llm_groq = ChatGroq(temperature=0.2, model_name="llama3-70b-8192", api_key = os.environ.get("GROQ_API_KEY"))

template = """
You are a SQL database expert. Based on the schema provided, and the message history, your role is to write a SQL query that answers the question/request.Always use the full financial amount for analysis. But when you provide the the results the amounts should only have two decimals.

Remember to UNNEST repeated records and make sure only to use existing fields in the schema:

schema: {schema}

Question: {question}

Message history: {messages}

SQL Query:
"""

prompt = ChatPromptTemplate.from_template(template)

hist = ChatMessageHistory()

db_path = '././data/northwind.db'

schema_file = 'src/schemas/northwind_schema.pkl'

def ensure_schema(schema_file, db_path):
    # Try to get the schema
    schema = get_schema(schema_file)
    if schema is None:
        # If the schema file does not exist, extract and save the schema
        schema = extract_db_schema(db_path)
        print(f"Schema extracted and saved to {schema_file}.")
    return schema

def get_schema_wrapper(_):
    return ensure_schema(schema_file, db_path)

def get_messages(_):
    print(hist.messages)
    return hist.messages

sql_response = (
    RunnablePassthrough.assign(schema=get_schema_wrapper, messages=get_messages)
    | prompt
    | llm_groq
    | StrOutputParser()
)

def extract_sql(input_text):
    # Check if the input contains triple backticks
    if '```' in input_text:
        # Regex to extract content within triple backticks
        pattern = re.compile(r'```(.*?)```', re.DOTALL)
        match = pattern.search(input_text)
        if match:
            return match.group(1).strip()  # Return the cleaned, extracted SQL
    # If no triple backticks are found, return the input as is
    return input_text.strip()

def execute_queries_with_retries(my_query, max_attempts=5):
    attempts = 0
    while attempts < max_attempts:
        attempts += 1
        print(f"Attempt {attempts} of {max_attempts}")
        # Invoke the external SQL service
        print("Generating the SQL")
        res = sql_response.invoke({"question": my_query})
        clean_sql = extract_sql(res)
        try:
            print("Attempting to run the query and convert it to a DataFrame")
            # Execute the SQL query using sqlite3 and convert the result to a DataFrame
            conn = sqlite3.connect(db_path)
            dataframe = pd.read_sql_query(clean_sql, conn)
            conn.close()
            print("Query executed successfully.")
            return dataframe
        except (sqlite3.DatabaseError, pd.io.sql.DatabaseError) as e:
            # Handle the custom BadRequestError
            error_message = str(e)
            print("Query failed with the following error:")
            print(error_message)
            hist.add_user_message(clean_sql + ': ' + error_message)
            if attempts == max_attempts:
                print("Reached maximum attempt limit. Stopping retries.")
                return None  # Return None if all retries fail
        except Exception as e:
            # Handle other general exceptions
            error_message = str(e)
            print("Query failed with the following error:")
            print(error_message)
            hist.add_user_message(clean_sql + ': ' + error_message)
            if attempts == max_attempts:
                print("Reached maximum attempt limit. Stopping retries.")
                return None  # Return None if all retries fail

if __name__ == '__main__':
    my_query = """
    Give me the name of the top 100 customers with highest purchase frequency but with under average AOV. 
Include frequency and aov
    """
    result = execute_queries_with_retries(my_query)
    if result is not None:
        print(f"Query Result:\n{result}")
    else:
        print("Failed to execute query after multiple attempts.")
