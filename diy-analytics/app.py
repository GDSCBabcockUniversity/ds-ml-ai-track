import streamlit as st
import pandas as pd
from llm import handle_query
from execute import execute_generated_code
import io

# Streamlit UI
st.title("DIY Analytics")

uploaded_file = st.file_uploader("Upload your CSV, EXCEL, or JSON dataset to get started!", type=["csv", "xlsx", "json"])


if uploaded_file:
    file_extension = uploaded_file.name.split('.')[-1].lower()

    if file_extension == "csv":
        data = pd.read_csv(uploaded_file)

    elif file_extension == "json":
        data = pd.read_json(uploaded_file)

    elif file_extension == "xlsx":
        data = pd.read_excel(uploaded_file)  
    
    else: 
        st.error(f"Unsupported file format: {file_extension}. Please upload a CSV or JSON file")
    
    st.write("#### Data Preview")
    st.dataframe(data.head())

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
    send, retry = st.columns(2)

    with send:
        send_button = st.button("Send")
    with retry:
        retry_button = st.button("Retry")


    with st.spinner("Insights cooking..."):
        if user_query or send_button or retry_button:
            code = handle_query(user_query, data)

            try:
                results, output = execute_generated_code(code, data)

                if output:
                    st.write(output)

                # Handle Matplotlib chart
                if "plt" in results:
                    st.pyplot(results["plt"].gcf())  

                # Handle string results (errors or other outputs)
                if isinstance(results, str): 
                    st.error(results)
                else:
                    st.toast("Code executed successfully.")
                    
            except Exception as e:
                st.error(f"Error executing code: {e}")

           # Optionally display the generated code
            if st.checkbox("Show code"):
                st.code(code, language="python")

            if st.checkbox("Download chart"):
                    format_options = ["PNG", "JPEG", "HTML"]
                    selected_format = st.selectbox("Select format:", format_options)

                    # Generate chart file in selected format
                    if selected_format in ["PNG", "JPEG"]:
                        buf = io.BytesIO()
                        results["plt"].savefig(buf, format=selected_format.lower())
                        buf.seek(0)
                        st.download_button(
                            label=f"Download Chart as {selected_format}",
                            data=buf,
                            file_name=f"chart.{selected_format.lower()}",
                            mime=f"image/{selected_format.lower()}",
                        )
                    elif selected_format == "HTML":
                        from matplotlib.backends.backend_svg import FigureCanvasSVG
                        buf = io.StringIO()
                        FigureCanvasSVG(results["plt"].gcf()).print_svg(buf)
                        html_content = f"<html><body>{buf.getvalue()}</body></html>"
                        st.download_button(
                            label="Download Chart as HTML",
                            data=html_content,
                            file_name="chart.html",
                            mime="text/html",
                        )
