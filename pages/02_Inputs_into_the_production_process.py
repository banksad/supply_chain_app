import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

# Data import

combined = pd.read_csv('data/combined.csv')
            
# Input intensity of products
# ----------------------------

# Inputs section

st.header('Inputs into the production process of goods and services')

st.markdown('This section examines what products (goods and services) need to be used in order to produce other products, and of these, what proportion are domestically produced and which imported. This utilises the ONS product-by-product tables, which are part of the Input-Output tables.')

with st.form(key='product_form'):
    combined_product = st.selectbox('Search for a product that you wish to analyse:',options=combined.sort_values(by='output product')['output product'].unique())
    pct_choice = st.selectbox('Choose whether to view data in £m or as proportions of total inputs needed to produce the product.',['Values (£m)','Percentage of total inputs'])
    
    submit_button = st.form_submit_button(label='Submit')

# Calculations

total_inputs = combined[combined['output product']==combined_product]['value'].sum()
domestic_inputs = combined[(combined['output product']==combined_product)&(combined['component']=='Domestically produced inputs')]['value'].sum()
imported_inputs = combined[(combined['output product']==combined_product)&(combined['component']=='Imported inputs')]['value'].sum()

st.subheader('Summary text')

st.write('The total production of {} required £{:,}m of goods and services to produce in 2018.'.format(combined_product.lower(),round(total_inputs,2)))
            
st.write('Of these inputs, £{:,}m were produced in the UK, and £{:,}m were imported.'.format(round(domestic_inputs,2),round(imported_inputs,2)))

# Total inputs

combined_subset = combined[combined['output product']==combined_product]

combined_subset['input_product_trun'] = combined_subset['input product'].apply(lambda x: x[:20]+'...') 

yarray = combined_subset.groupby('input_product_trun')['value'].sum().sort_values(ascending=False).head(20).index.tolist()

combined_subset = combined_subset[combined_subset['input_product_trun'].isin(yarray)]

# Chart choice

st.subheader('Chart')

if pct_choice == 'Values (£m)':

    st.markdown('##### Domestically produced and imported inputs used in the domestic production of {} products'.format(combined_product))    
    fig = px.bar(combined_subset, color='component', y='input_product_trun', x='value',
                        labels={
                            'component':'Category',
                            'input_product_trun': 'Product',
                            'value': 'Value (£m)'
                        },
                height=600,
                hover_name='input product',
                hover_data={'value':':.1f',
                            'component':False,
                            'input_product_trun':False
                            }
                )
    fig.update_layout(barmode='stack',
                      margin=dict(l=100))

    fig.update_yaxes(categoryorder='array', categoryarray=yarray[::-1])

    config = {'displayModeBar': True}

    st.plotly_chart(fig, use_container_width=True, config=config)

else:
    
    st.markdown('##### Domestically produced and imported inputs used in the domestic production of {} products'.format(combined_product))    
    fig = px.histogram(combined_subset, 
                        color='component',
                        y='input_product_trun', 
                        x='value',
                        barnorm='percent',
                            labels={
                                'component':'Category',
                                'input_product_trun':'Product',
                                'sum of value (normalised as percent)': 'percentage of total inputs'
                            },
            height=600,
            hover_name='input product',
            hover_data={
                        'component':False,
                        'input_product_trun':False
                        })

    fig.update_layout(xaxis_title='Percentage of total inputs')

    fig.update_yaxes(categoryorder='array', categoryarray=yarray[::-1])

    config = {'displayModeBar': True}

    st.plotly_chart(fig, use_container_width=True, config=config)
        
see_import_data3 = st.expander('You can click here to see the raw data. Data are currently ordered in descending order of the value of inputs used in the production of a product.')

data_viewer = combined_subset.rename(columns={'component':'Component',
                                              'input product':'Input Product',
                                              'output product':'Output Product',
                                              'value':'Value (£m)',
                                              'proportion':'Proportion'})

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

    st.table(data=data_viewer[['Component','Input Product','Output Product','Value (£m)']].sort_values(by='Value (£m)',ascending=False))