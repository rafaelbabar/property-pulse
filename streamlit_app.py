import streamlit as st
import pandas as pd
#D:\OneDrive\Desktop\Projects>streamlit run property-pulse-v6.py
def propertypulse():
    st.title("Property Sales - Manchester")
    st.subheader("1 January 2020 - last month")
    
    df = pd.read_csv("ppd_data.csv", encoding="utf-8-sig")
    
    search = st.radio("Please select a criteria", 
                      ("Price", "Post Code", "Property Type", "Transaction Category"))
    
    def make_clickable(link):
        return f'<a href="{link}" target="_blank">{link}</a>'
    
    if search == "Post Code":
        enterpostcode = st.text_input("Please enter a post code")
        if st.button("Check Post Code"):
            filtered_df = df[df['postcode'] == enterpostcode]
            if not filtered_df.empty:
                st.dataframe(filtered_df[['price_paid', 'deed_date', 'saon', 'paon', 'street']])
                filtered_df['linked_data_uri'] = filtered_df['linked_data_uri'].apply(make_clickable)
                st.markdown(filtered_df[['linked_data_uri']].to_html(escape=False), unsafe_allow_html=True)
            else:
                st.write("No results found for the entered post code.")
    
    elif search == "Property Type":
        property_types = df['property_type'].unique().tolist()
        ptsearch = st.selectbox("Please select a property type", [""] + property_types)
        st.write("F - Flat")
        st.write("O - Other")
        st.write("T - Terraced")
        st.write("D - Detached")
        st.write("S - Semi Detached")
        if ptsearch:
            filtered_df = df[df['property_type'] == ptsearch]
            if not filtered_df.empty:
                st.dataframe(filtered_df[['price_paid', 'deed_date', 'saon', 'paon', 'street', 'postcode']])
                filtered_df['linked_data_uri'] = filtered_df['linked_data_uri'].apply(make_clickable)
                st.markdown(filtered_df[['linked_data_uri']].to_html(escape=False), unsafe_allow_html=True)
            else:
                st.write("No results found for the selected property type.")
    
    elif search == "Transaction Category":
        transaction_categories = df['transaction_category'].unique().tolist()
        tcsearch = st.selectbox("Please select a transaction category", [""] + transaction_categories)
        st.write("B - Additional price paid transaction")
        st.write("S - Standard price paid transaction")
        if tcsearch:
            filtered_df = df[df['transaction_category'] == tcsearch]
            if not filtered_df.empty:
                st.dataframe(filtered_df[['price_paid', 'deed_date', 'saon', 'paon', 'street', 'postcode']])
                filtered_df['linked_data_uri'] = filtered_df['linked_data_uri'].apply(make_clickable)
                st.markdown(filtered_df[['linked_data_uri']].to_html(escape=False), unsafe_allow_html=True)
            else:
                st.write("No results found for the selected transaction category.")

propertypulse()
