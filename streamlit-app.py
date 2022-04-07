"""
# author = Andy Banks
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

st.set_page_config(layout="wide")

# Data import

iot_use = pd.read_csv('data/iot_cleaned.csv')
imports_use = pd.read_csv('data/imports_use_cleaned.csv')
combined = pd.read_csv('data/combined.csv')
cpa_classification = pd.read_csv('data/cpa_classification.csv')

# Page design
st.title('Supply Chain Analysis')

st.markdown('This is a prototype dashboard to present a range of publicly available information on supply chains.')
st.markdown('The dashboard uses publicly available information on the Input Output tables to understand the inputs into the production process.')
st.markdown('The text and charts automatically update depending on the product chosen in the sidebar.')
st.markdown('You can find the source code [here](https://github.com/banksad/supply_chain_app). Feel free to do a pull request :smile:')

iot_product = st.sidebar.selectbox('Search for a product that you wish to analyse',set(list(imports_use['output product'])))
import_product = iot_product
combined_product = iot_product

st.sidebar.markdown('')
if st.sidebar.button('Click here to see the cpa product classification'):
    st.sidebar.dataframe(data=cpa_classification)
else:
    st.sidebar.write('')
            
# Input intensity of products
# ----------------------------

# Calculations

total_inputs = combined[combined['output product']==combined_product]['value'].sum()
domestic_inputs = combined[(combined['output product']==combined_product)&(combined['component']=='domestic use')]['value'].sum()
imported_inputs = combined[(combined['output product']==combined_product)&(combined['component']=='imports')]['value'].sum()

# Inputs section

st.subheader('Inputs into the production process: Analysis of {} products'.format(iot_product.lower()))

st.markdown('This section examines the types products that are used in the production process, and the degree to which these products are imported.')

st.markdown('The total production of {} products required **£{}m** of raw inputs in 2018. Of this, **£{}m** was domestically produced inputs (i.e. from other UK producers), while **£{}m** was imported from inputs'.format(
    combined_product.lower(),total_inputs,domestic_inputs,imported_inputs))

# Total inputs

st.markdown('This section examines both domestically produced and imported products that are used in the domestic production of the product selected.')

combined_subset = combined[combined['output product']==combined_product]
combined_subset = combined_subset[combined_subset['proportion']>0]

st.markdown("")
see_import_data3 = st.expander('You can click here to see the raw data 👉')
with see_import_data3:
    st.dataframe(data=combined_subset[['component','input product','value']].sort_values(by='value',ascending=False))
        
st.markdown('*Imported and domestically produced products used in the domestic production of {} products*'.format(import_product.lower()))

fig = px.treemap(combined_subset, path=['component','input product'], values='value',
                color='value',color_continuous_scale='OrRd')
fig.update_layout(uniformtext=dict(minsize=7, mode='hide'))
st.plotly_chart(fig, use_container_width=True)
                        
# Effects of an increase in demand on whole economy output

st.subheader('Effects of an increase in demand for {} on the economy'.format(iot_product.lower()))

st.markdown('The Input Output tables show the indirect and direct effects of an increase in demand for a product on the whole economy and employment income (compensation of employees)')
