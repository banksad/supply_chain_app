"""
# author = Andy Banks
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

# Data import

iot_use = pd.read_csv('data/iot_cleaned.csv')
imports_use = pd.read_csv('data/imports_use_cleaned.csv')
combined = pd.read_csv('data/combined.csv')

# Page design
st.title('Supply Chain Analysis')

st.markdown('This is a prototype dashboard to present a range of publicly available information on supply chains.')
st.markdown('The dashboard uses publicly available information on the Input Output tables to understand the inputs into the production process.')
st.markdown('The text and charts automatically update depending on the product chosen in the sidebar.')
st.markdown('You can find the source code [here](https://github.com/banksad/supply_chain_app). Feel free to do a pull request :smile:')

iot_product = st.sidebar.selectbox('Search for a product that you wish to analyse',set(list(imports_use['output product'])))
import_product = iot_product
combined_product = iot_product
            
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

chart_choice = st.selectbox('Choose whether to view domestically produced inputs, imported inputs, or both', ['Both','Domestically produced','Imported'])

col1, col2 = st.columns(2)

# Domestic input intensity of products

if chart_choice=='Domestically produced':
    
    with col1:

        st.markdown('This section examines the types of domestically produced inputs that are used in the domestic production of the product selected')

        iot_subset = iot_use[iot_use['output product']==iot_product]
        iot_subset = iot_subset[iot_subset['proportion']>0]

        st.markdown("")
        see_iot_data = st.expander('You can click here to see the raw data 👉')
        with see_iot_data:
            st.dataframe(data=iot_subset[['domestic input requirements','value']])

        legend_indicator1 = st.selectbox('Add / remove legend',['No legend','Add Legend'])

    with col2:
        
        st.markdown('*Domestically produced inputs used in the UK production of {} products*'.format(iot_product.lower()))
        
        if legend_indicator1=='No legend':
            fig = px.pie(iot_subset, values='proportion', names='domestic input requirements')
            fig.update_traces(textposition='inside',hoverlabel_namelength=10)
            fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide', showlegend=False)
            st.plotly_chart(fig)
        else:
            fig = px.pie(iot_subset, values='proportion', names='domestic input requirements')
            fig.update_traces(textposition='inside',hoverlabel_namelength=10)
            fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide', showlegend=True)
            st.plotly_chart(fig)

elif chart_choice=='Imported':

# Import intensity of products

    with col1:

        st.markdown('This section examines the types of imported products that are used in the domestic production of the product selected')

        import_subset = imports_use[imports_use['output product']==import_product]
        import_subset = import_subset[import_subset['proportion']>0]

        st.markdown("")
        see_import_data2 = st.expander('You can click here to see the raw data 👉')
        with see_import_data2:
            st.dataframe(data=import_subset[['import requirements','value']])
            
        legend_indicator2 = st.selectbox('Add / remove legend',['No legend','Add Legend'])

    with col2:
        
        st.markdown('*Imported products used in the domestic production of {} products*'.format(import_product.lower()))
        
        if legend_indicator2=='No legend':
            fig = px.pie(import_subset, values='proportion', names='import requirements')
            fig.update_traces(textposition='inside')
            fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide', showlegend=False)
            st.plotly_chart(fig)
        else: 
            fig = px.pie(import_subset, values='proportion', names='import requirements')
            fig.update_traces(textposition='inside')
            fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide', showlegend=True)
            st.plotly_chart(fig)
            
else:

# Total inputs

    with col1:
        st.markdown('This section examines both domestically produced and imported products that are used in the domestic production of the product selected')

        combined_subset = combined[combined['output product']==combined_product]
        combined_subset = combined_subset[combined_subset['proportion']>0]

        st.markdown("")
        see_import_data3 = st.expander('You can click here to see the raw data 👉')
        with see_import_data3:
            st.dataframe(data=combined_subset[['input product','value']])

    with col2:
        
        st.markdown('*Imported and domestically produced products used in the domestic production of {} products*'.format(import_product.lower()))
        
        fig = px.sunburst(combined_subset, path=['component','input product'], values='value')
        st.plotly_chart(fig)
            
            
# Effects of an increase in demand on whole economy output

st.subheader('Effects of an increase in demand for {} on the economy'.format(iot_product.lower()))

st.markdown('The Input Output tables show the indirect and direct effects of an increase in demand for a product on the whole economy and employment income (compensation of employees)')
