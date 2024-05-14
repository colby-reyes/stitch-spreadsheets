# streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(
    page_title="Spreadsheet Stitcher",
    page_icon=":thread:", #"https://www.logolynx.com/images/logolynx/4f/4f42c461be2388aca949521bbb6a64f1.gif",
    layout="wide",
)



def stitch_spreadsheets(file_list:list):
    
    df_list = []
    success_list = []
    for i in file_list:
        if i.name.endswith('xls') or i.name.endswith('xlsx'):
            try:
                df_list.append(pd.read_excel(i))
                success_list.append(i.name)
            except Exception as excel_error:
                st.toast(f"Skipping file: {i.name}\n\n {excel_error}")
        else:
            try:
                df_list.append(pd.read_csv(i))
                success_list.append(i.name)
            except Exception as csv_error:
                st.toast(f"Skipping file {i.name}:\n\n {csv_error}")
    try:
        final_df = pd.concat(df_list)
        pre_dedup_len = len(final_df)
        if st.session_state.deduplicate_tf is True:
            st.session_state.final_df = final_df.drop_duplicates(keep="first",ignore_index=True)
            removed_lines = pre_dedup_len - len(st.session_state.final_df)
            st.toast(f"Removed {removed_lines} duplicate entries")
        else:
            st.session_state.final_df = final_df

        
    except Exception as concat_error:
        st.error(f"The following error occurred in stitching the files:\n {concat_error}")

    success_msg = '\n\n * ' + '\n\n * '.join(success_list)
    st.session_state.button_state = "secondary"

    notification_container = st.container().empty()
    with notification_container:
        st.success(f"File(s) read and stitched successfully: {success_msg}")
        time.sleep(1)
        notification_container.empty()
    st.toast("Done!")

def set_button_primary():
    st.session_state.button_state = "primary"
    

def main():
    st.title(body=":thread: Spreadsheet Stitcher")

    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []
    
    if "final_df" not in st.session_state:
        st.session_state.final_df = None
    
    if "deduplicate_tf" not in st.session_state:
        st.session_state.deduplicate_tf = False

    if "button_state" not in st.session_state:
        st.session_state.button_state = "primary"
    
    st.session_state.uploaded_files = st.file_uploader(label="Select spreadsheets to combine:",type=['xls','xlsx','csv'],accept_multiple_files=True,on_change=set_button_primary)

    if len(st.session_state.uploaded_files) > 0:
        btn_type = "secondary" if st.session_state.final_df is None else "primary"
        c0, c1, c2, c3 = st.columns([1,2,3,1])
        with c1:
            st.session_state. deduplicate_tf = st.checkbox("Deduplicate?",value=False,help="Check this box to remove duplicates when stitching the spreadsheets together. Only do this if you are sure that duplciate lines should be removed!")
        with c2:
            st.button("Stitch Spreadsheets", on_click=stitch_spreadsheets, args=[st.session_state.uploaded_files], type=st.session_state.button_state)
        # st.write(st.session_state.uploaded_files)
    
    if st.session_state.final_df is not None:
        st.dataframe(st.session_state.final_df)


if __name__ == "__main__":
    main()
