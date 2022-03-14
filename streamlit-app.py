"""
# My first app
Here's our first attempt at using data to create an app
"""

import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

st.set_page_config(layout="centered")

# Data import
country_imports = pd.read_json("data/top_10.json")
iosut_section_edges = pd.read_csv('data/iosut_section_edges.csv')
iosut_long = pd.read_csv('data/iosut_long.csv')

# Page design
st.title('Supply Chain Analysis')

st.sidebar.markdown('This is a prototype dashboard to present a range of publicly available information on supply chains.')
            
st.sidebar.markdown('You can find the source code [here](https://github.com/banksad/supply_chain_app). Feel free to do a pull request :smile:')

# Industry to industry relationships

st.subheader('Industry to industry relationships')

st.markdown("**Select level of detail you want to analyze:** 👇")

detail = st.radio('Pick a level of detail',['Section','114 industry','All sections','All 114 industries'])

st.markdown("**Select industries you want to analyze:** 👇")

if detail=='114 industry': 

    industry = st.multiselect('Pick a set of industries',set(sorted(list(iosut_long['variable']))))

    st.markdown("")
    st.markdown("The network graph below shows the value of inputs that the given industry uses from other industries")

    iosut_section_edges1 = iosut_long[iosut_long['variable'].isin(industry)]

    G = nx.from_pandas_edgelist(
        iosut_section_edges1, target='variable', source='product_stripped', 
        edge_attr = 'value',       # this adds weighting to the edges based on transaction values
        create_using = nx.DiGraph  # this gives the network directionality
    )

    edge_weights = [G.edges[edge]['value'] for edge in G.edges]
    edge_widths = [weight / max(edge_weights) * 10 for weight in edge_weights]

    fig = plt.figure(figsize=(8,8))
    ax = plt.axes()

    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color = 'royalblue')
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='black', width=edge_widths)
    nx.draw_networkx_labels(G, pos, font_color = 'white')

    st.pyplot(fig, use_container_width=False)
    
elif detail=='Section':

    industry = st.multiselect('Pick a set of industries',set(sorted(list(iosut_section_edges['industry']))))

    st.markdown("")
    st.markdown("The network graph below shows the value of inputs that the given industry uses from other industries")

    iosut_section_edges1 = iosut_section_edges[iosut_section_edges['industry'].isin(industry)]

    G = nx.from_pandas_edgelist(
        iosut_section_edges1, target='industry', source='product_stripped', 
        edge_attr = 'value',       # this adds weighting to the edges based on transaction values
        create_using = nx.DiGraph  # this gives the network directionality
    )

    edge_weights = [G.edges[edge]['value'] for edge in G.edges]
    edge_widths = [weight / max(edge_weights) * 10 for weight in edge_weights]

    fig = plt.figure(figsize=(8,8))
    ax = plt.axes()

    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color = 'royalblue')
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='black', width=edge_widths)
    nx.draw_networkx_labels(G, pos, font_color = 'white')

    st.pyplot(fig, use_container_width=False)    

if detail=='All sections': 

    st.markdown("")
    st.markdown("The network graph below shows the value of inputs that the given industry uses from other industries")

    iosut_section_edges1 = iosut_section_edges

    G = nx.from_pandas_edgelist(
        iosut_section_edges1, target='industry', source='product_stripped', 
        edge_attr = 'value',       # this adds weighting to the edges based on transaction values
        create_using = nx.DiGraph  # this gives the network directionality
    )

    edge_weights = [G.edges[edge]['value'] for edge in G.edges]
    edge_widths = [weight / max(edge_weights) * 2 for weight in edge_weights]

    fig = plt.figure(figsize=(8,8))
    ax = plt.axes()

    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=200, node_color = 'royalblue')
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='black', width=edge_widths)
    nx.draw_networkx_labels(G, pos, font_color = 'white')

    st.pyplot(fig, use_container_width=False)

if detail=='All 114 industries': 

    st.markdown("")
    st.markdown("The network graph below shows the value of inputs that the given industry uses from other industries")

    iosut_section_edges1 = iosut_long

    G = nx.from_pandas_edgelist(
        iosut_section_edges1, target='variable', source='product_stripped', 
        edge_attr = 'value',       # this adds weighting to the edges based on transaction values
        create_using = nx.DiGraph  # this gives the network directionality
    )

    edge_weights = [G.edges[edge]['value'] for edge in G.edges]
    edge_widths = [weight / max(edge_weights) * 2 for weight in edge_weights]

    fig = plt.figure(figsize=(8,8))
    ax = plt.axes()

    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=50, node_color = 'royalblue')
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color='black', width=edge_widths)
    nx.draw_networkx_labels(G, pos, font_color = 'white', font_size=2)

    st.pyplot(fig, use_container_width=False)

# Imports section

st.subheader('Imports')

st.markdown("**Select a product and country you want to analyze:** 👇")

product_static = st.selectbox('Pick a product',set(list(country_imports['TEXT'])))

country_static = st.selectbox('Pick a country',['France','Germany'])

st.image('data/vis.png')

# Exports section
# -----------------

st.subheader('Exports')

st.markdown("**Select a country you want to analyze:** 👇")

country = st.selectbox('Pick a country',set(list(country_imports['Name'])))

st.markdown('This is a list of the top ten exports for the country selected')

export_subset = country_imports[country_imports['Name']==country][['VALUE','TEXT','Name']].sort_values(by=['VALUE'])

fig = px.bar(export_subset, x='VALUE', y='TEXT', width=1600)
st.plotly_chart(fig, use_container_width=False)