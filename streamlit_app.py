import streamlit as st
import pandas as pd
#D:\OneDrive\Desktop\Projects>streamlit run property-pulse-v4.py

def propertypulse():
    st.title("Property Sales - Manchester")
    st.subheader("1 January 2020 - last month")
    
    # Read the CSV file once
    df = pd.read_csv("ppd_data.csv", encoding="utf-8-sig")
    
    search = st.radio("Please select a criteria", 
                              ("Price", "Post Code", "Property Type", "Transaction Category"))
    
    if search == "Post Code":
        enterpostcode = st.text_input("Please enter a post code")
        if st.button("Check Post Code"):
            filtered_df = df[df['postcode'] == enterpostcode]
            if not filtered_df.empty:
                st.dataframe(filtered_df[['price_paid', 'deed_date', 'saon', 'paon', 'street', 'linked_data_uri']])
            else:
                st.write("No results found for the entered post code.")
    
    elif search == "Property Type":
        st.write("F - Flat")
        st.write("O - Other")
        st.write("T - Terraced")
        st.write("D - Detached")
        st.write("S - Semi Detached")
        property_types = df['property_type'].unique().tolist()
        ptsearch = st.selectbox("Please select a property type", [""] + property_types)
        if ptsearch:
            filtered_df = df[df['property_type'] == ptsearch]
            if not filtered_df.empty:
                st.dataframe(filtered_df[['price_paid', 'deed_date', 'saon', 'paon', 'street', 'postcode', 'linked_data_uri']])
            else:
                st.write("No results found for the selected property type.")
    
    elif search == "Transaction Category":
        st.write("B - Additional price paid transaction")
        st.write("A - Standard price paid transaction")
        transaction_categories = df['transaction_category'].unique().tolist()
        tcsearch = st.selectbox("Please select a transaction category", [""] + transaction_categories)
        if tcsearch:
            filtered_df = df[df['transaction_category'] == tcsearch]
            if not filtered_df.empty:
                st.dataframe(filtered_df[['price_paid', 'deed_date', 'saon', 'paon', 'street', 'postcode', 'linked_data_uri']])
            else:
                st.write("No results found for the selected transaction category.")
    
    elif search == "Price":
        min_price = st.number_input("Please enter a minimum price", value=0)
        max_price = st.number_input("Please enter a maximum price", value=1000000)
        if st.button("Check Price Range"):
            filtered_df = df[(df['price_paid'] >= min_price) & (df['price_paid'] <= max_price)]
            if not filtered_df.empty:
                st.dataframe(filtered_df[['price_paid', 'deed_date', 'saon', 'paon', 'street', 'postcode', 'linked_data_uri']])
            else:
                st.write("No results found for the selected price range.")

propertypulse()
