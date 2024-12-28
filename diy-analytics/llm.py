from groq import Groq
import streamlit as st
from summary import summarize_data, get_columns
import ast
import re


# Initialize Groq API
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
groq_client = Groq(api_key=GROQ_API_KEY)

def get_relevant_columns(query, column_names):
    system_message = (
        "You are a professional data analyst proficient in Python programming.\n"
        f"Based on the following list of column names:\n{column_names}\n"
        f"If you were to manipulate the data under those columns to answer the question: '{query}'.\n"
        "What columns will you use? Return a python list containing only the column names you will need to answer the question."
        "Output format: python list [] containing relevant column names. ONLY. No prioir comments or text. just python list only. Nothing else." 
        )

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": query}
    ]

    response = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages
    )

    list_as_string = response.choices[0].message.content.strip()

    try:
        relevant_columns = ast.literal_eval(list_as_string)
        if not isinstance(relevant_columns, list):
            raise ValueError("The output is not a list.")
    except Exception as e:
        raise ValueError(f"Failed to parse the LLM response into a Python list: {e}")

    return relevant_columns


def ask_llm(query, data_summary):
    system_message = (
        f"You are a professional data analyst proficient in Python programming.\n"
        f"Based on the following dataset summary:\n{data_summary}\n"
        "Provide clean python code using pandas and matplotlib (only the code, nothing else) that when executed will:\n"
        f" Answer the user's question: '{query}'.\n"
        "Note that the unique values of each column are supposed to guide you on how to generate value-specific code/ insights."
        "The code should contain a visualization that is well labelled and inprint whatever text you need to add on the visualization fig."
        "Assume the dataset has been read into a dataframe called df."
        "If the query involves generating a chart (e.g., bar plot), please ensure the chart displays no more than 10 categories (top or bottom)."
        "If the user specifically requests to show all categories, include that in the code. If no specific instruction is provided, limit the chart to the top or bottom 10 categories based on the count or value"
    )

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": query}
    ]

    response = groq_client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages
    )

    code_generated =  response.choices[0].message.content
    code_match = re.search(r"```(?:\w*\n)?(.*?)```", code_generated, re.DOTALL)
    executable_code = code_match.group(1).strip() if code_match else response.strip()

    return executable_code


def handle_query(query, data):
    columns = get_columns(data)
    relevant_columns = get_relevant_columns(query, columns)
    summary_data = summarize_data(data, relevant_columns)
    code = ask_llm(query, summary_data)

    return code
