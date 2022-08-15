import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

# Data import

detailed_effects = pd.read_csv('data/detailed_effects.csv')

# Effects of an increase in demand on whole economy output

st.subheader('Effects of a change in demand for a product on the economy')

st.markdown('The Input Output tables show the indirect and direct effects of an increase in demand for a product on the whole economy and employment income (compensation of employees).')

multiplier_product = st.selectbox('Select a product',options=detailed_effects.sort_values(by='product')['product'].unique())

change = st.number_input('Input change in demand for the product (£m)')

# Total calculations

effects_subset = detailed_effects[detailed_effects['product']==multiplier_product]
total_effects = effects_subset[effects_subset['factor']=='total impact']

total_gva = (effects_subset[(effects_subset['factor']=='total impact')&(effects_subset['variable']=='Gross value added')]['value']*change).values[0]

total_imports = (effects_subset[(effects_subset['factor']=='total impact')&(effects_subset['variable']=='Use of imported products, cif')]['value']*change).values[0]

total_coe = (effects_subset[(effects_subset['factor']=='total impact')&(effects_subset['variable']=='Compensation of employees')]['value']*change).values[0]

total_go = (effects_subset[(effects_subset['factor']=='total impact')&(effects_subset['variable']=='Output')]['value']*change).values[0]

total_effects['total_effects'] = total_effects['value'] * change

# Writing

if change<0:
    
    st.write('The change in gross value added is -£{:,}m'.format(round(total_gva*-1, 2)))

    st.write('This is because domestic output changes by -£{:,}m, and there is a change in imports of -£{:,}m'.format(round(total_go*-1,2),round(total_imports*-1,2)))

    st.write('Employee compensation would change by -£{:,}m', round(total_coe*-1,2))

    # Add chart

    st.markdown('##### Total effects of a change to final use of -£{:,}m for {}'.format(round(change*-1,2),multiplier_product.lower()))    
    fig = px.bar(total_effects, y='total_effects', x='factor',
                    labels={
                        'total_effects':'Total effect',
                        'factor': 'Component'
                    })
    st.plotly_chart(fig, use_container_width=True)
    
else:

    st.write('The change in gross value added is £{:,}m'.format(round(total_gva, 2)))

    st.write('This is because domestic output changes by £{:,}m, and there is a change in imports of £{:,}m'.format(round(total_go,2),round(total_imports,2)))

    st.write('Employee compensation would change by £{:,}m'.format(round(total_coe,2)))

    # Add chart

    st.markdown('##### Total effects of a change to final use of £{:,}m for {}'.format(round(change,2),multiplier_product.lower()))    
    fig = px.bar(total_effects, x='total_effects', y='factor',
                    labels={
                        'total_effects':'Total effect',
                        'factor': 'Component'
                    })
    st.plotly_chart(fig, use_container_width=True)

