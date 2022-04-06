"""
# My first app
Here's our first attempt at using data to create an app
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

# Data import

iot_use = pd.read_csv('data/iot_cleaned.csv')
imports_use = pd.read_csv('data/imports_use_cleaned.csv')

# Page design
st.title('Supply Chain Analysis')

st.sidebar.markdown('This is a prototype dashboard to present a range of publicly available information on supply chains.')

iot_product = st.sidebar.selectbox('Search for a product that you wish to analyse',set(list(imports_use['output product'])))
import_product = iot_product
            
st.sidebar.markdown('You can find the source code [here](https://github.com/banksad/supply_chain_app). Feel free to do a pull request :smile:')

# Domestic input intensity of products

st.subheader('Domestic inputs used in UK production')

st.markdown('This section examines the types of domestically produced inputs that are used to produce the product selected')

iot_subset = iot_use[iot_use['output product']==iot_product]
iot_subset = iot_subset[iot_subset['proportion']>0]

fig = px.pie(iot_subset, values='proportion', names='domestic input requirements')
fig.update_traces(textposition='inside')
fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
st.plotly_chart(fig)

# Import intensity of products

st.subheader('Imported products used in domestic production')

st.markdown('This section examines the types of imported products that are used to domestically produce the product selected')

import_subset = imports_use[imports_use['output product']==import_product]
import_subset = import_subset[import_subset['proportion']>0]

fig = px.pie(import_subset, values='proportion', names='import requirements')
fig.update_traces(textposition='inside')
fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
st.plotly_chart(fig)