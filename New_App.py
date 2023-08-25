#Import Modules
import re
import difflib
import requests
import numpy as np
import pandas as pd
import streamlit as st
from gsheetsdb import connect
from google.oauth2 import service_account
from streamlit_tags import st_tags
from streamlit_lottie import st_lottie
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode


#Set Page Layout
st.set_page_config(page_title="Kipi Catalog",layout='wide')

#------------------Fetching GIF-----------------------------------------------
@st.cache(ttl=1200)
def lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

home_gif = lottie_url('https://assets3.lottiefiles.com/packages/lf20_l3j1mflq.json')

#------------------------------------------Header-------------------------------------------
st.markdown(""" <style> .font_header {
        font-size:40px ; font-family: 'Cooper Black'; color: #fafafa;} 
        </style> """, unsafe_allow_html=True)
st.markdown('<p class="font_header" align="center">Kipi Project Catalog</p>', unsafe_allow_html=True)

#------------Google Sheet Connection Establishing--------------------
# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets",],
)
conn = connect(credentials=credentials)

# Perform SQL query on the Google Sheet.
@st.cache(ttl=1200)
def run_query_with_headers(query):
    rows = conn.execute(query)
    headers = [column[0] for column in rows.description]
    data = rows.fetchall()
    return headers, data

#----------------------Client Project Data Fetch-----------------  
try:
    #reading spreadsheet
    sheet_url = st.secrets["all_industries"]
    headers, data = run_query_with_headers(f'SELECT * FROM "{sheet_url}"')
    client_df = pd.DataFrame(data, columns=headers)
except:
    st.error("There is issue in the network connection. Try after sometime!")
    st.stop()
    
#handling missing value
client_df.fillna('', inplace=True)
