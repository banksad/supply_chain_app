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