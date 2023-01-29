import streamlit as st
import pandas as pd
import plotly.express as px

# Data import

detailed_effects = pd.read_csv('data/detailed_effects.csv')

# Effects of an increase in demand on whole economy output

st.subheader('Effects of a change in final use for a product on the economy')

st.markdown("""

To meet an increase in final use for a product, more of the inputs of that product need to be produced or imported. This effect continues up the supply chain, leading to a change in total use for products.

This change in total output is captured by effects. They also capture changes to other inputs into the production process, such as compensation of employees and gross operating surplus.

This tab allows the user to model the total effect of a change in final use on the economy.

The effects published by ONS are sometimes referred to as Type 1. They include the impact on production of a change in final use (direct impact) and the supply chain impacts stemming from the initial change in final use (indirect impact).

However, they do not include induced impacts (i.e. Type 2 effects), which cover changes to a households spending from employment changes linked to a change in final use. In addition, the model assumes that the structure of the economy doesn't change and that any additional inputs are available.

The results of the model are therefore most robust with relatively small changes to final use.

""")

with st.form(key='effects_form'):
    multiplier_product = st.selectbox('Select a product',options=detailed_effects.sort_values(by='Product')['Product'].unique())
    change = st.number_input('Input change in final use for the product (£m)', step=1, format='%d')

    submit_button = st.form_submit_button(label='Submit')

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
    
    st.write('The change in gross value added is -£{:,}m'.format(round(total_gva*-1, 1)))

    st.write('There is a corresponding change in imports of -£{:,}m'.format(round(total_imports*-1,1)))

    st.write('Employee compensation would change by -£{:,}m'.format(round(total_coe*-1,1)))

    # Add chart

    st.markdown('##### Total effects of a change to final use of -£{:,}m for {}'.format(round(change*-1,1),multiplier_product))    
    fig = px.bar(total_effects, y='variable', x='total_effects',
                    labels={
                        'total_effects':'Total effect (£m)',
                        'variable': 'Component'
                    },
                    hover_data={'total_effects':':.1f',
                                'variable':False})

    fig.update_layout(margin=dict(l=300))

    config = {'displayModeBar': True}

    st.plotly_chart(fig, use_container_width=True, config=config)
    
else:

    st.write('The change in gross value added from the selected change in final use is £{:,}m. There is a corresponding change in imports of £{:,}m, and employee compensation would change by £{:,}m'.format(round(total_gva, 2),round(total_imports,2),round(total_coe,2)))

    # Add chart

    st.markdown('##### Total effects of a change to final use of £{:,}m for {}'.format(round(change,1),multiplier_product))    
    fig = px.bar(total_effects, y='variable', x='total_effects',
                    labels={
                        'total_effects':'Total effect (£m)',
                        'variable': 'Component'
                    },
                    hover_data={'total_effects':':.1f',
                                'variable':False})
    
    fig.update_layout(margin=dict(l=300))

    config = {'displayModeBar': True}

    st.plotly_chart(fig, use_container_width=True, config=config)

