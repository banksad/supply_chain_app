"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import altair as alt
import vega_datasets as vg

st.set_page_config(layout="wide")

# Data import
country_imports = pd.read_json("data/top_10.json")
country_total = pd.read_csv("data/UNSDfinal.csv")

# Page design
st.title('Supply Chain Analysis')

st.subheader('Streamlit App by [Andy Banks](https://github.com/banksad)')

st.markdown('This is a prototype dashboard to present a range of publicly available information on supply chains.')
            
st.markdown('You can find the source code [here](https://github.com/banksad/supply_chain_app). Feel free to do a pull request :smile:')

# Imports section

st.subheader('Imports')

st.markdown("**Select a product you want to analyze:** 👇")

product = st.selectbox('Pick a product',set(list(country_imports['TEXT'])))

# Exports section
# -----------------

st.subheader('Exports')

st.markdown("**Select a country you want to analyze:** 👇")

country = st.selectbox('Pick a country',set(list(country_imports['Name'])))

st.markdown('This is a list of the top ten exports for the country selected')

export_subset = country_imports[country_imports['Name']==country][['VALUE','TEXT','Name']].sort_values(by=['VALUE'])

# Bar chart

c = alt.Chart(export_subset).mark_bar().encode(
     alt.X('VALUE', axis=alt.Axis(title='Value of exports')),
     alt.Y('TEXT', axis=alt.Axis(title='Product exported'))
     ).configure_axis(
       labelFontSize=8
     ).configure_view(
       continuousWidth=1350
     )

st.altair_chart(c)

# World map

topo_countries = alt.topo_feature(vg.data.world_110m.url, 'countries')

c = alt.Chart(topo_countries).mark_geoshape(
    fill='lightgray',
    stroke='white'
).project(
    "equirectangular"
).properties(
    width=500,
    height=300
)

st.altair_chart(c)