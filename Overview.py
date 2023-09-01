import streamlit as st

st.title('Input Output Analytical Tables (IOATs) Dashboard')

st.header("Overview")

# Sidebar

st.markdown('This prototype dashboard contains a range of publicly available information on the Input Output Analytical tables (IOATs) produced by the Office for National Statistics (ONS).')
st.markdown('The IOATs show what products and primary inputs are used to make other products and satisfy final use. They can also be used to estimate the impact of changes in final use.')
st.markdown('You can find interactive content on this in the different sidebar pages.')

st.markdown(
"""
A summary of the three tabs is set out below:

- **Industry use of goods and services**: This tab presents information on the extent to which different industries in the economy use specific goods and services in their production processes.

- **Inputs into the production process**: This section examines what products (goods and services) need to be used in order to produce other products, and of these, what proportion are domestically produced or imported.

- **Effect of a final use change**: This tab shows the effect of a change in final use for a product on the economy. It allows the user to retrieve the estimated impact on variables such as Gross Value Added (GVA) or imports.
"""
)
st.markdown('The text and charts within each page will automatically update depending on the options chosen in the selection boxes. The data refer to 2018.')