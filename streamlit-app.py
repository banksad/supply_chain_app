"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(layout="wide")

# Data import
country_imports = pd.read_json("data/top_10.json")

# Page design
st.title('Supply Chain Analysis')

st.subheader('Streamlit App by [Andy Banks](https://github.com/banksad)')

st.markdown('This is a prototype dashboard to present a range of publicly available information on supply chains.')
            
st.markdown('You can find the source code [here](https://github.com/banksad/supply_chain_app). Feel free to do a pull request :smile:')

# Imports section

st.subheader('Imports')

st.sidebar.markdown("**Select a product you want to analyze:** 👇")

product = st.sidebar.selectbox('Pick a country',set(list(country_imports['TEXT'])))

st.subheader('Exports')

st.sidebar.markdown("**Select a country you want to analyze:** 👇")

country = st.sidebar.selectbox('Pick a country',set(list(country_imports['Name'])))

st.markdown('This is a list of the top ten exports for the country selected')

export_subset = country_imports[country_imports['Name']==country][['VALUE','TEXT','Name']].sort_values(by=['VALUE'])

c = alt.Chart(export_subset).mark_bar().encode(
     x='VALUE', 
     y='TEXT'
     )

st.altair_chart(c, use_container_width=True)