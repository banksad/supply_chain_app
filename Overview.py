import streamlit as st

st.markdown("# Overview")

# Sidebar

st.markdown('This is a prototype dashboard to present a range of publicly available information on Input Output tables.')
st.markdown('Different pages can be clicked on in the sidebar. These each contain interactive content relating to the Input Output tables produced by the Office for National Statistics (ONS)')
st.markdown(
"""
Summaries of the three tabs are set out below:
- **Industry use of goods and services**: This tab presents information on the extent to which different industries in the economy use specific goods and services in their production processes.

- **Inputs into the production process**: This section examines what products (goods and services) need to be used in order to produce other products, and of these, what proportion are imported.

- **Effect of a demand change**: This tab shows the effect of a change in final use for a product on the economy. It allows the user to retrieve the estimated impact on variables such as Gross Value Added (GVA) or imports.
"""
)
st.markdown('The text and charts within each page will automatically update depending on the options chosen in the selection boxes.')