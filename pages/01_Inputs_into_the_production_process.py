import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

# Data import

combined = pd.read_csv('data/combined.csv')
cpa_classification = pd.read_csv('data/cpa_classification.csv')
            
# Input intensity of products
# ----------------------------

# Inputs section

st.subheader('Inputs into the production process')

st.markdown('This section examines the products that are used in the production process, and the proportion of these products that are imported.')

combined_product = st.selectbox('Search for a product that you wish to analyse:',options=combined.sort_values(by='output product')['output product'].unique())

# Calculations

total_inputs = combined[combined['output product']==combined_product]['value'].sum()
domestic_inputs = combined[(combined['output product']==combined_product)&(combined['component']=='Domestically produced inputs')]['value'].sum()
imported_inputs = combined[(combined['output product']==combined_product)&(combined['component']=='Imported inputs')]['value'].sum()

st.write('The total production of {} required £{}m of goods and services to produce in 2018.'.format(combined_product.lower(),round(total_inputs,0)))
            
st.write('Of these inputs, £{}m were produced in the UK, and £{}m were imported.'.format(round(domestic_inputs,0),round(imported_inputs,0)))

# Total inputs

combined_subset = combined[combined['output product']==combined_product]
combined_subset = combined_subset[combined_subset['proportion']>0]

# Chart choice

chart_choice = st.selectbox('Choose whether to view total inputs, or a breakdown of domestically produced and imported inputs.',['Total inputs','Domestic / Imported breakdown'])
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
        fig = px.bar(combined_subset, y='input product', x='value')
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.markdown('##### Total inputs used in the domestic production of {} products'.format(combined_product.lower()))
        fig = px.bar(combined_subset, y='input product', x='proportion')
        st.plotly_chart(fig, use_container_width=True)
        
see_import_data3 = st.expander('You can click here to see the raw data 👉')
with see_import_data3:
    st.dataframe(data=combined_subset[['component','input product','value','proportion']].sort_values(by='value',ascending=False))