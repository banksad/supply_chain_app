import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

# Data import

detailed_effects = pd.read_csv('data/detailed_effects.csv')

# Effects of an increase in demand on whole economy output

st.subheader('Effects of a change in demand for a product on the economy')

st.markdown('This tab shows the effect of a change in final use for a product on the economy. It allows the user to retrieve the estimated impact on variables such as Gross Value Added (GVA) or imports')

multiplier_product = st.selectbox('Select a product',options=detailed_effects.sort_values(by='Product')['Product'].unique())

change = st.number_input('Input change in demand for the product (£m)')

# Total calculations

effects_subset = detailed_effects[detailed_effects['Product']==multiplier_product]
total_effects = effects_subset[effects_subset['factor']=='total impact']

total_gva = (effects_subset[(effects_subset['factor']=='total impact')&(effects_subset['variable']=='Gross value added')]['value']*change).values[0]

total_imports = (effects_subset[(effects_subset['factor']=='total impact')&(effects_subset['variable']=='Use of imported products, cif')]['value']*change).values[0]

total_coe = (effects_subset[(effects_subset['factor']=='total impact')&(effects_subset['variable']=='Compensation of employees')]['value']*change).values[0]

total_go = (effects_subset[(effects_subset['factor']=='total impact')&(effects_subset['variable']=='Output')]['value']*change).values[0]

total_effects['total_effects'] = total_effects['value'] * change

# Writing

if change<0:
    
    st.write('The change in gross value added is -£{:,}m'.format(round(total_gva*-1, 2)))

    st.write('There is a corresponding change in imports of -£{:,}m'.format(round(total_imports*-1,2)))

    st.write('Employee compensation would change by -£{:,}m'.format(round(total_coe*-1,2)))

    # Add chart

    st.markdown('##### Total effects of a change to final use of -£{:,}m for {}'.format(round(change*-1,2),multiplier_product.lower()))    
    fig = px.bar(total_effects, y='total_effects', x='variable',
                    labels={
                        'total_effects':'Total effect (£m)',
                        'variable': False
                    })

    config = {'displayModeBar': True}

    st.plotly_chart(fig, use_container_width=True, config=config)
    
else:

    st.write('The change in gross value added is £{:,}m'.format(round(total_gva, 2)))

    st.write('There is a corresponding change in imports of £{:,}m'.format(round(total_imports,2)))

    st.write('Employee compensation would change by £{:,}m'.format(round(total_coe,2)))

    # Add chart

    st.markdown('##### Total effects of a change to final use of £{:,}m for {}'.format(round(change,2),multiplier_product.lower()))    
    fig = px.bar(total_effects, y='total_effects', x='variable',
                    labels={
                        'total_effects':'Total effect (£m)',
                        'variable': False
                    })
    
    config = {'displayModeBar': True}

    st.plotly_chart(fig, use_container_width=True, config=config)

