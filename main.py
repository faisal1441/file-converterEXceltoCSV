import streamlit as st
import pandas as pd
from io import BytesIO

# Set up our App
st.set_page_config(page_title="File Converter", layout='wide')
st.title("File Converter and Cleaner")
st.write("Upload CSV or Excel files, clean data, and convert formats.")

# File Uploader
files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]  # Get file extension
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        # Display info about the file
        st.subheader(f"{file.name} - Preview")
        st.dataframe(df.head())

        # Data Cleaning Options
        if st.checkbox(f"Remove Duplicates - {file.name}"):
            df = df.drop_duplicates()
            st.success("Duplicates Removed!")
            st.dataframe(df.head())

        if st.checkbox(f"Fill Missing Values - {file.name}"):
            df.fillna(df.select_dtypes(include=['number']).mean(), inplace=True)
            st.success('Missing values filled with mean')
            st.dataframe(df.head())

        if st.checkbox(f"Show Chart - {file.name}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        format_choice = st.radio(f"Convert {file.name} to:", ["csv", "Excel"], key=file.name)

        if st.button(f"Download {file.name} as {format_choice}"):
            output = BytesIO()
            if format_choice == 'csv':
                df.to_csv(output, index=False)
                mime = "text/csv"
                new_name = file.name.replace(ext, 'csv')
            else: 
                df.to_excel(output, index=False, engine='openpyxl')
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.replace(ext, "xlsx")

            output.seek(0)
            st.download_button(
                label="Download file",
                data=output,  # Pass the file data here
                file_name=new_name,
                mime=mime
            )
            
        st.success("Processing Complete!")