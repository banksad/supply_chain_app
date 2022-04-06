"""
# My first app
Here's our first attempt at using data to create an app
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

st.set_page_config(layout="centered")

# Data import

imports_use = pd.read_csv('data/imports_use_pxp_cleaned.csv')

# Page design
st.title('Supply Chain Analysis')

st.sidebar.markdown('This is a prototype dashboard to present a range of publicly available information on supply chains.')
            
st.sidebar.markdown('You can find the source code [here](https://github.com/banksad/supply_chain_app). Feel free to do a pull request :smile:')

# Import intensity of products

st.subheader('Import content of domestically produced products')

st.markdown("**Select level of detail you want to analyze:** 👇")

product = st.multiselect('Search for a product',set(list(imports_use['output product'])))

import_subset = imports_use[imports_use['output product']==product]
import_subset = import_subset[import_subset['proportion']>0]

#fig = px.pie(import_subset, values='proportion', names='import requirements')
#st.plotly_chart(fig)