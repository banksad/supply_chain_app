import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

# Data import

combined = pd.read_csv('data/industry_use_cleaned.csv')
cpa_classification = pd.read_csv('data/cpa_classification.csv')
            
# Input intensity of products
# ----------------------------

# Inputs section

st.header('How much do different industries use of a given product?')

st.markdown('This section examines the relative importance of a product to every industry.')

combined_product = st.selectbox('Search for a product that you wish to analyse:',options=combined.sort_values(by='input requirements')['input requirements'].unique())

combined_subset = combined[combined['input requirements']==combined_product]
combined_subset = combined_subset[combined_subset['proportion']>0]

# Chart choice

st.subheader('Chart')
    
st.markdown('##### Proportion of total intermediate consumption from {} products '.format(combined_product.lower()))
fig = px.bar(combined_subset, y='industry', x='proportion',
                labels={
                    'industry': 'Industry',
                    'proportion': 'Proportion of total intermediate consumption'
                })
fig.update_layout(barmode='stack',yaxis={'categoryorder':'total ascending'})
fig.layout.xaxis.tickformat = ',.0%'
# overwrite tick labels    
fig.update_layout(
    yaxis = {
     'tickmode': 'array',
     'ticktext': combined_subset['industry'].str.slice(10).tolist(),
    }
)
st.plotly_chart(fig, use_container_width=True)
        
see_import_data3 = st.expander('You can click here to see the raw data')
with see_import_data3:
    st.dataframe(data=combined_subset[['industry','input requirements','proportion']].sort_values(by='proportion',ascending=False))