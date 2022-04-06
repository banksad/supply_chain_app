"""
# My first app
Here's our first attempt at using data to create an app
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(layout="centered")

# Data import


# Page design
st.title('Supply Chain Analysis')

st.sidebar.markdown('This is a prototype dashboard to present a range of publicly available information on supply chains.')
            
st.sidebar.markdown('You can find the source code [here](https://github.com/banksad/supply_chain_app). Feel free to do a pull request :smile:')

# Industry to industry relationships

st.subheader('Industry to industry relationships')

st.markdown("**Select level of detail you want to analyze:** 👇")

detail = st.radio('Pick a level of detail',['Section','114 industry','All sections','All 114 industries'])

