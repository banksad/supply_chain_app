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

def truncate(x):

    return x[:20]+'...'

combined_subset['industry_trun'] = combined_subset['industry'].apply(lambda x: truncate(x)) 

# Chart choice

st.subheader('Chart')
    
st.markdown('##### Proportion of total intermediate consumption from {} products '.format(combined_product.lower()))
fig = px.bar(combined_subset, y='industry_trun', x='proportion',
                labels={
                    'industry_trun': 'Industry',
                    'proportion': 'Proportion of total intermediate consumption'
                },
                height=600,
                hover_name='industry',
                hover_data={'proportion':':.1%',
                            'industry':False,
                            'industry_trun':False}
                )
fig.update_layout(barmode='stack',yaxis={'categoryorder':'total ascending'})
fig.layout.xaxis.tickformat = ',.0%'

config = {'displayModeBar': True}

st.plotly_chart(fig, use_container_width=True, config=config)
        
see_import_data3 = st.expander('You can click here to see the raw data. Data are currently ordered in descending order or proportion of total intermediate consumption attributable to a product.')

data_viewer = combined_subset.rename(columns={'industry':'Industry','input requirements':'Input Product','proportion':'Proportion of total intermediate consumption'})

with see_import_data3:
    # CSS to inject contained in a string
    hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """

    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    st.table(data=data_viewer[['Industry','Input Product','Proportion of total intermediate consumption']].sort_values(by='Proportion of total intermediate consumption',ascending=False))