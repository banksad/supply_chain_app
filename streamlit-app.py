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

combined = pd.read_csv('data/combined.csv')
cpa_classification = pd.read_csv('data/cpa_classification.csv')

# Sidebar

st.sidebar.markdown('This is a prototype dashboard to present a range of publicly available information on supply chains.')
st.sidebar.markdown('The dashboard uses publicly available information on the Input Output tables to understand the inputs into the production process.')
st.sidebar.markdown('The text and charts automatically update depending on the options chosen in the selection boxes.')
st.sidebar.markdown('You can find the source code [here](https://github.com/banksad/supply_chain_app). Feel free to do a pull request :smile:')

st.sidebar.markdown('')
if st.sidebar.button('Click here to see the cpa product classification'):
    st.sidebar.dataframe(data=cpa_classification)
else:
    st.sidebar.write('')

# Page design
st.title('Supply Chain Analysis')
            
# Input intensity of products
# ----------------------------

# Inputs section

st.subheader('Inputs into the production process')

st.markdown('This section examines the types products that are used in the production process, and the degree to which these products are imported.')

st.markdown('Search for a product that you wish to analyse')

combined_product = st.selectbox('',set(list(combined['output product'])))

# Calculations

total_inputs = combined[combined['output product']==combined_product]['value'].sum()
domestic_inputs = combined[(combined['output product']==combined_product)&(combined['component']=='Domestically produced inputs')]['value'].sum()
imported_inputs = combined[(combined['output product']==combined_product)&(combined['component']=='Imported inputs')]['value'].sum()

st.markdown('The total production of {} products required **£{}m** of raw inputs in 2018. Of this, **£{}m** was domestically produced inputs (i.e. from other UK producers), while **£{}m** was imported inputs.'.format(
    combined_product.lower(),total_inputs,domestic_inputs,imported_inputs))

# Total inputs

combined_subset = combined[combined['output product']==combined_product]
combined_subset = combined_subset[combined_subset['proportion']>0]
        
st.markdown('Choose whether to view total inputs, or a breakdown of domestically produced and imported inputs')

col1, col2 = st.columns(2)

with col1:
    chart_choice = st.selectbox('',['Total inputs','Domestic / Imported breakdown'])
with col2:
    pct_choice = st.selectbox('',['Values (£m)','Percentage of total inputs'])

if chart_choice == 'Domestic / Imported breakdown':
    
    if pct_choice == 'Values (£m)':
    
        st.markdown('##### Domestically produced and imported inputs used in the domestic production of {} products'.format(combined_product.lower()))    
        fig = px.treemap(combined_subset, path=['component','input product'], values='value',
                        color='value',color_continuous_scale='OrRd')
        st.plotly_chart(fig, use_container_width=True)

    else:
        
        st.markdown('##### Domestically produced and imported inputs used in the domestic production of {} products'.format(combined_product.lower()))    
        fig = px.treemap(combined_subset, path=['component','input product'], values='proportion',
                        color='proportion',color_continuous_scale='OrRd')
        st.plotly_chart(fig, use_container_width=True)

else:
    
    if pct_choice =='Values (£m)':
    
        st.markdown('##### Total inputs used in the domestic production of {} products'.format(combined_product.lower()))
        fig = px.treemap(combined_subset, values='value',
                        color='value',color_continuous_scale='OrRd')
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        
        st.markdown('##### Total inputs used in the domestic production of {} products'.format(combined_product.lower()))
        fig = px.treemap(combined_subset, values='proportion',
                        color='proportion',color_continuous_scale='OrRd')
        st.plotly_chart(fig, use_container_width=True)
        
see_import_data3 = st.expander('You can click here to see the raw data 👉')
with see_import_data3:
    st.dataframe(data=combined_subset[['component','input product','value','proportion']].sort_values(by='value',ascending=False))
                        
# Effects of an increase in demand on whole economy output

st.subheader('Effects of an increase in demand for {} on the economy'.format(combined_product.lower()))

st.markdown('The Input Output tables show the indirect and direct effects of an increase in demand for a product on the whole economy and employment income (compensation of employees)')
