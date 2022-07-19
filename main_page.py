import streamlit as st

st.markdown("# Main page")
st.sidebar.markdown("# Main page")

# Sidebar

st.markdown('This is a prototype dashboard to present a range of publicly available information on supply chains.')
st.markdown('The text and charts automatically update depending on the options chosen in the selection boxes.')
st.markdown('You can find the source code [here](https://github.com/banksad/supply_chain_app)')

st.markdown('')
if st.button('Click here to see the cpa product classification'):
    st.dataframe(data=cpa_classification)
else:
    st.write('')