import streamlit as st
import pandas as pd
import plotly.express as px

# Data import

combined = pd.read_csv('data/combined_pi.csv')
            
# Input intensity of products
# ----------------------------

# Inputs section

st.header('How do industries use goods and services in the production process?')

st.markdown("""This tab presents information on the extent to which different industries in the economy use specific goods and services in their production processes. In choosing a product, the chart will show how much that product makes up of each industry's total input into its production process.""")

with st.form(key='product_form'):
    combined_product = st.selectbox('Search for a product that you wish to analyse:',options=combined.sort_values(by='input requirements')['input requirements'].unique())
    pct_choice = st.selectbox('Choose whether to view data in £m or as proportions of total intermediate consumption needed to produce the product.',['Values (£m)','Percentage of total inputs'])
    
    submit_button = st.form_submit_button(label='Submit')

# Calculations

total_inputs = combined[combined['input requirements']==combined_product]['value'].sum()
domestic_inputs = combined[(combined['input requirements']==combined_product)&(combined['component']=='Domestically produced inputs')]['value'].sum()
imported_inputs = combined[(combined['input requirements']==combined_product)&(combined['component']=='Imported inputs')]['value'].sum()

# Total inputs

combined_subset = combined[combined['input requirements']==combined_product]

combined_subset['industry_trun'] = combined_subset['industry'].apply(lambda x: x[:20]+'...') 

# Summary text

st.subheader('Summary text')

st.write('In 2018, £{:,}m of {} were used in the production of goods and services across all UK industries.'.format(round(total_inputs,2),combined_product))
            
st.write('Of these inputs, £{:,}m were produced in the UK, and £{:,}m were imported.'.format(round(domestic_inputs,2),round(imported_inputs,2)))


# Chart choice

st.subheader('Chart')

if pct_choice == 'Values (£m)':

    yarray = combined_subset.groupby('industry_trun')['value'].sum().sort_values(ascending=False).head(20).index.tolist()
    combined_subset = combined_subset[combined_subset['industry_trun'].isin(yarray)]

    st.markdown('##### Total intermediate consumption of {} products'.format(combined_product))    
    fig = px.bar(combined_subset, color='component', y='industry_trun', x='value',
                        labels={
                            'component':'Category',
                            'industry_trun': 'Industry',
                            'value': 'Value (£m)'
                        },
                height=600,
                hover_name='industry',
                hover_data={'value':':.1f',
                            'component':False,
                            'industry_trun':False
                            }
                )
    fig.update_layout(barmode='stack',
                      margin=dict(l=200))

    fig.update_yaxes(categoryorder='array', categoryarray=yarray[::-1])

    config = {'displayModeBar': True}

    st.plotly_chart(fig, use_container_width=True, config=config)

else:

    yarray = combined_subset.groupby('industry_trun')['proportion_total'].sum().sort_values(ascending=False).head(20).index.tolist()
    combined_subset = combined_subset[combined_subset['industry_trun'].isin(yarray)]
    combined_subset['proportion_total'] = combined_subset['proportion_total']*100
    
    st.markdown('##### Intermediate consumption of {} products: percentage domestically produced and imported'.format(combined_product))    
    fig = px.bar(combined_subset, 
                        color='component',
                        y='industry_trun', 
                        x='proportion_total',
                            labels={
                                'component':'Category',
                                'industry_trun':'Industry',
                                'proportion_total': 'Percentage of total intermediate consumption'
                            },
            height=600,
            hover_name='industry',
            hover_data={
                        'proportion_total':':.1f',
                        'component':False,
                        'industry_trun':False
                        })

    fig.update_layout(barmode='stack',
                      xaxis_title='Percentage of total intermediate consumption',
                      margin=dict(l=200))

    fig.update_yaxes(categoryorder='array', categoryarray=yarray[::-1])

    config = {'displayModeBar': True}

    st.plotly_chart(fig, use_container_width=True, config=config)
        
see_import_data3 = st.expander('You can click here to see the raw data. Data are currently ordered in descending order of the value of intermediate consumption')

data_viewer = combined_subset.rename(columns={'component':'Component',
                                              'input requirements':'Product',
                                              'industry':'Industry',
                                              'value':'Value (£m)'})

data_viewer = data_viewer.round({'Value (£m)':1})
data_viewer = data_viewer[['Component','Product','Industry','Value (£m)']].sort_values(by='Value (£m)',ascending=False)
data_viewer = data_viewer.astype({'Value (£m)':'str'})

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

    st.table(data=data_viewer)