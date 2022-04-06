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

st.sidebar.markdown('This is a prototype dashboard to present a range of publicly available information on supply chains.')

iot_product = st.sidebar.selectbox('Search for a product that you wish to analyse',set(list(imports_use['output product'])))
import_product = iot_product
combined_product = iot_product
            
st.sidebar.markdown('You can find the source code [here](https://github.com/banksad/supply_chain_app). Feel free to do a pull request :smile:')

# Effects of an increase in demand on whole economy output

st.subheader('Effects of an increase in demand for {} on the economy'.format(iot_product.lower()))

st.markdown('The Input Output tables show the indirect and direct effects of an increase in demand for a product on the whole economy and employment income (compensation of employees)')

# Input intensity of products

st.subheader('Inputs into the production process: Analysis of {} products'.format(iot_product.lower()))

st.markdown('This section examines the types products that are used in the production process, and the degree to which these products are imported')

chart_choice = st.selectbox('Choose whether to view domestically produced inputs, imported inputs, or both', ['Both','Domestically produced','Imported'])

col1, col2 = st.columns(2)

# Domestic input intensity of products

if chart_choice=='Domestically produced':
    
    with col1:
        st.subheader('Domestic inputs used in the UK production of {} products'.format(iot_product.lower()))

        st.markdown('This section examines the types of domestically produced inputs that are used in the domestic production of the product selected')

        iot_subset = iot_use[iot_use['output product']==iot_product]
        iot_subset = iot_subset[iot_subset['proportion']>0]

        st.markdown("")
        see_iot_data = st.expander('You can click here to see the raw data 👉')
        with see_iot_data:
            st.dataframe(data=iot_subset)

        legend_indicator1 = st.selectbox('Add / remove legend',['No legend','Add Legend'])

    with col2:
        
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
        st.subheader('Imported products used in the domestic production of {} products'.format(import_product.lower()))

        st.markdown('This section examines the types of imported products that are used in the domestic production of the product selected')

        import_subset = imports_use[imports_use['output product']==import_product]
        import_subset = import_subset[import_subset['proportion']>0]

        st.markdown("")
        see_import_data2 = st.expander('You can click here to see the raw data 👉')
        with see_import_data2:
            st.dataframe(data=import_subset)
            
        legend_indicator2 = st.selectbox('Add / remove legend',['No legend','Add Legend'])

    with col2:
        
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
        st.subheader('Imported and domestically produced products used in the domestic production of {} products'.format(import_product.lower()))

        st.markdown('This section examines both domestically produced and imported products that are used in the domestic production of the product selected')

        combined_subset = combined[combined['output product']==combined_product]
        combined_subset = combined_subset[combined_subset['proportion']>0]

        st.markdown("")
        see_import_data3 = st.expander('You can click here to see the raw data 👉')
        with see_import_data3:
            st.dataframe(data=combined_subset)
            
        legend_indicator3 = st.selectbox('Add / remove legend',['No legend','Add Legend'])

    with col2:
        
        if legend_indicator3=='No legend':
            fig = px.sunburst(combined_subset, path=['component','input product'], values='value')
            #fig.update_traces(textposition='inside')
            #fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide', showlegend=False)
            st.plotly_chart(fig)
        else: 
            fig = px.sunburst(combined_subset, path=['component','input product'], values='value')
            #fig.update_traces(textposition='inside')
            #fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide', showlegend=True)
            st.plotly_chart(fig)