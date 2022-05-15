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
detailed_effects = pd.read_csv('data/detailed_effects.csv')
cpa_classification = pd.read_csv('data/cpa_classification.csv')

# Sidebar

st.sidebar.markdown('This is a prototype dashboard to present a range of publicly available information on supply chains.')
st.sidebar.markdown('The text and charts automatically update depending on the options chosen in the selection boxes.')
st.sidebar.markdown('You can find the source code [here](https://github.com/banksad/supply_chain_app)')

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

combined_product = st.selectbox('Search for a product that youn wish to analyse:',set(list(combined['output product'])))

# Calculations

total_inputs = combined[combined['output product']==combined_product]['value'].sum()/1000
domestic_inputs = combined[(combined['output product']==combined_product)&(combined['component']=='Domestically produced inputs')]['value'].sum()/1000
imported_inputs = combined[(combined['output product']==combined_product)&(combined['component']=='Imported inputs')]['value'].sum()/1000

st.write('The total production of {} required £{}bn of raw inputs in 2018.'.format(combined_product.lower(),round(total_inputs,2)))
            
st.write('Of this, £{}bn were domestically produced inputs (i.e. from other UK producers.'.format(round(domestic_inputs,2)))
     
st.write('By contrast, £{}bn were imported inputs.'.format(round(imported_inputs,2)))

# Total inputs

combined_subset = combined[combined['output product']==combined_product]
combined_subset = combined_subset[combined_subset['proportion']>0]

col1, col2 = st.columns(2)

with col1:
    chart_choice = st.selectbox('Choose whether to view total inputs, or a breakdown of domestically produced and imported inputs.',['Total inputs','Domestic / Imported breakdown'])
with col2:
    pct_choice = st.selectbox('Choose whether to view data in £m or proportions of total inputs.',['Values (£m)','Percentage of total inputs'])

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
        fig = px.treemap(combined_subset, path=['input product'], values='value',
                        color='value',color_continuous_scale='OrRd')
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.markdown('##### Total inputs used in the domestic production of {} products'.format(combined_product.lower()))
        fig = px.treemap(combined_subset, path=['input product'], values='proportion',
                        color='proportion',color_continuous_scale='OrRd')
        st.plotly_chart(fig, use_container_width=True)
        
see_import_data3 = st.expander('You can click here to see the raw data 👉')
with see_import_data3:
    st.dataframe(data=combined_subset[['component','input product','value','proportion']].sort_values(by='value',ascending=False))
                        
# Effects of an increase in demand on whole economy output

st.subheader('Effects of a change in demand for a product on the economy')

st.markdown('The Input Output tables show the indirect and direct effects of an increase in demand for a product on the whole economy and employment income (compensation of employees).')

multiplier_product = st.selectbox('Select a product',set(list(detailed_effects['product'])))

change = st.number_input('Input change in demand for the product (£m)')

# Calculations

effects_subset = detailed_effects[detailed_effects['product']==multiplier_product]

total_gva = (effects_subset[(effects_subset['factor']=='total impact')&(effects_subset['variable']=='Gross value added')]['value']*change).values[0]

total_imports = (effects_subset[(effects_subset['factor']=='total impact')&(effects_subset['variable']=='Use of imported products, cif')]['value']*change).values[0]

total_coe = (effects_subset[(effects_subset['factor']=='total impact')&(effects_subset['variable']=='Compensation of employees')]['value']*change).values[0]

# Writing

if change<0:
    
    st.write('The change in gross value added is -£', round(total_gva*-1, 2), 'm')

    st.write('This is because there is a corresponding change to imports of -£', round(total_imports*-1,2), 'm')

    st.write('Employee compensation would change by -£', round(total_coe*-1,2), 'm')
    
else:

    st.write('The change in gross value added is £{}m'.format(round(total_gva, 2)))

    st.write('This is because there is a corresponding change to imports of £{}m'.format(round(total_imports,2)))

    st.write('Employee compensation would change by £{}m'.format(round(total_coe,2)))