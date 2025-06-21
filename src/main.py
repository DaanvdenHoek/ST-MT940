import streamlit as st
from src.parser import parse_mt940, df_to_xlsx_bytes
from src.options import option_map

OUTPUT_FILE_NAME = "SwiftTransactions.xlsx"


def run():
    def reset_converted_file() -> None:
        st.session_state.converted_file = None

    if "converted_file" not in st.session_state:
        reset_converted_file()

    st.title("Swift MT904 Parser")

    files = st.file_uploader(
        label="Select file(s) to parse",
        accept_multiple_files=True,
        type="swi",
        on_change=reset_converted_file,
    )

    processing_label = st.radio(
        "Choose output format:",
        options=list(option_map.keys()),
        help="""
        - **One Excel file with multiple worksheets**: Each uploaded file becomes its own tab (worksheet) in one Excel file.  
        - **One Excel file with all data in a single worksheet**: All data is merged into one sheet.  
        - **Separate Excel files per source file**: You’ll get multiple Excel files, one for each input file.
        """,
        on_change=reset_converted_file,
    )

    if files:
        if st.button("Parse"):
            file_names = [file.name.rsplit(".")[0] for file in files]
            if len(set(file_names)) != len(file_names):
                st.error("Duplicate filenames found")
            else:
                dfs = [parse_mt940(file) for file in files]
                processing_option = option_map[processing_label]
                data = df_to_xlsx_bytes(dfs, file_names, processing_option)
                st.session_state.converted_file = data
                st.success("File parsed and ready for download.")

        if st.session_state.converted_file:
            st.download_button(
                label="Download",
                data=st.session_state.converted_file,
                file_name=OUTPUT_FILE_NAME,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                on_click=reset_converted_file,
            )
