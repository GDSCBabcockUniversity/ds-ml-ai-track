import streamlit as st
import pandas as pd
from summary import summarize_data
from llm import ask_llm
from execute import execute_generated_code
import re

# Streamlit UI
st.title("DIY Analytics")

uploaded_file = st.file_uploader("Upload your CSV or JSON dataset to get started!", type=["csv","json"])


if uploaded_file:
## spliting the filename into parts using the period
    file_extension = uploaded_file.name.split('.')[-1].lower()

    ## Checking for various file formats and adjusing reading methods based on them
    if file_extension == "csv":
        data = pd.read_csv(uploaded_file)
        summary_data = summarize_data(data)
        st.write("#### Data Preview")
        st.dataframe(data.head())

    elif file_extension == "json":
        data = pd.read_json(uploaded_file)
        summary_data = summarize_data(data)
        st.write("#### Data Preview")
        st.dataframe(data.head())
    
    else: 
        ## Displaying error in the case of an unsupported file format
        st.error(f"Unsupported file format: {file_extension}. Please upload a CSV or JSON file")


    if st.checkbox("Show Data Summary"):
        missing_values, duplicated_values, summary_statistics = st.tabs(["Missing Values", "Duplicated Values", "Summary Statistics"])
        total_missing_values_by_column = data.isnull().sum()
        missing_values.write(total_missing_values_by_column)
        missing_values.write(f"There are {total_missing_values_by_column.sum()} missing values in your dataset.")

        total_duplicated_values_by_column = data.duplicated().sum()
        duplicated_values.write(total_duplicated_values_by_column)
        duplicated_values.write(f"There are {total_duplicated_values_by_column.sum()} duplicated values in your dataset.")

        summary_statistics.write("#### Summary Statistics")
        summary_statistics.dataframe(data.describe())


    st.header("Chat with your data!")
    user_query = st.text_input("Ask a question about your dataset:")
    
    with st.spinner("Insights cooking..."):
        if user_query:
            response = ask_llm(user_query, summary_data)
            code_match = re.search(r"```(?:\w*\n)?(.*?)```", response, re.DOTALL)
            code = code_match.group(1).strip() if code_match else response.strip()
            try:
                results, output = execute_generated_code(code, data)

                if output:
                    st.write(output) 
                if "plt" in results:
                    st.pyplot(results["plt"].gcf())  

                if isinstance(results, str): 
                    st.error(results)
                else:
                    st.toast("Code executed successfully.")
                
            except Exception as e:
                st.error(f"Error executing code: {e}")

            if st.checkbox("Show code"):
                st.code(code, language="python")
