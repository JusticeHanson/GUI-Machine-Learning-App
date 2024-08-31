import streamlit as st
import pandas as pd
import os  # Import os module to check file existence

# Configure the page
st.set_page_config(
    page_title='History',
    page_icon='📜',
    layout='wide'
)

# --------- Add custom CSS to adjust the width of the sidebar
st.markdown(""" 
    <style> 
        section[data-testid="stSidebar"] { width: 200px !important; }
    </style> """, unsafe_allow_html=True)

def history_page():
    # Set header for page
    st.title('History')

    # Check if the file exists before attempting to load it
    if os.path.exists('./data/history.csv'):
        data = pd.read_csv('./data/history.csv')
        st.dataframe(data)
    else:
        st.write("No history data available.")

if __name__ == '__main__':
    history_page()