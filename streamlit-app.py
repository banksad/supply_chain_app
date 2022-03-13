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

# Sidebar

st.sidebar.text('')
st.sidebar.text('')
st.sidebar.text('')

st.sidebar.markdown("**First select a country you want to analyze:** 👇")

country = st.sidebar.selectbox('Pick a country',set(list(country_imports['Name'])))

df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

df

st.subheader('Exports')

st.markdown('This is a list of the top ten exports for the country selected')

export_subset = country_imports[country_imports['Name']==country][['VALUE','TEXT','Name']]

c = alt.Chart(export_subset).mark_bar().encode(
     x='TEXT', 
     y='VALUE'
     )

st.altair_chart(c, use_container_width=True)