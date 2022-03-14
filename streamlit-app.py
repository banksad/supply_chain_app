"""
# My first app
Here's our first attempt at using data to create an app
"""

import streamlit as st
import pandas as pd
import altair as alt
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="wide")

# Data import
country_imports = pd.read_json("data/top_10.json")
iosut_section_edges = pd.read_csv('data/iosut_section_edges.csv')

# Page design
st.title('Supply Chain Analysis')

st.subheader('Streamlit App by [Andy Banks](https://github.com/banksad)')

st.markdown('This is a prototype dashboard to present a range of publicly available information on supply chains.')
            
st.markdown('You can find the source code [here](https://github.com/banksad/supply_chain_app). Feel free to do a pull request :smile:')

# Industry to industry relationships

st.subheader('Industry to industry relationships')

st.markdown("**Select an Industry you want to analyze:** 👇")

industry = st.selectbox('Pick an industry',set(list(iosut_section_edges['industry'])))

G = nx.from_pandas_edgelist(
    iosut_section_edges, target='industry', source='product_stripped', 
    edge_attr = 'value',       # this adds weighting to the edges based on transaction values
    create_using = nx.DiGraph  # this gives the network directionality
)

G

fig = plt.figure(figsize=(16, 16))
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_size=500, node_color = 'royalblue')
nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='black')
nx.draw_networkx_labels(G, pos, font_color = 'white')

st.pyplot(fig)


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
