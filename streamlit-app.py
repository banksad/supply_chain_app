"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# Data import
country_imports = pd.read_json("data/top_10.json")
country_csv = pd.read_csv('data/UNSDfinal.csv')

# Page design
st.title('Supply Chain Analysis')

st.subheader('Streamlit App by [Andy Banks](https://github.com/banksad)')

st.markdown('This is a prototype dashboard to present a range of publicly available information on supply chains.')
            
st.markdown('You can find the source code [here](https://github.com/banksad/supply_chain_app). Feel free to do a pull request :smile:')

df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

df