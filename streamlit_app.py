#D:\OneDrive\Desktop\Projects>streamlit run property-pulse-v8.py
import streamlit as st
import pandas as pd

def propertypulse():
    st.title("Property Sales - Manchester")
    st.subheader("1 January 2020 - last month")
    
    df = pd.read_csv("ppd_data.csv", encoding="utf-8-sig")
    
    search = st.radio("Please select a criteria", 
                      ("Price", "Post Code", "Property Type", "Transaction Category"))
    
    def make_clickable(link):
        return f'<a href="{link}" target="_blank">{link}</a>'
    
    def display_filtered_data(filtered_df):
        st.dataframe(filtered_df[['price_paid', 'deed_date', 'saon', 'paon', 'street', 'postcode']])
        row_selection = st.selectbox("Select a row to view the link", filtered_df.index)
        if row_selection is not None:
            selected_link = filtered_df.loc[row_selection, 'linked_data_uri']
            st.markdown(make_clickable(selected_link), unsafe_allow_html=True)

    if search == "Post Code":
        enterpostcode = st.text_input("Please enter a post code")
        if 'filtered_df_postcode' not in st.session_state:
            st.session_state['filtered_df_postcode'] = pd.DataFrame()
        if st.button("Check Post Code"):
            st.session_state['filtered_df_postcode'] = df[df['postcode'] == enterpostcode]
        filtered_df = st.session_state['filtered_df_postcode']
        if not filtered_df.empty:
            display_filtered_data(filtered_df)
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
                display_filtered_data(filtered_df)
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
                display_filtered_data(filtered_df)
            else:
                st.write("No results found for the selected transaction category.")
    
    elif search == "Price":
        min_price = st.number_input("Please enter a minimum price", value=0)
        max_price = st.number_input("Please enter a maximum price", value=1000000)
        if 'filtered_df_price' not in st.session_state:
            st.session_state['filtered_df_price'] = pd.DataFrame()
        if st.button("Check Price Range"):
            st.session_state['filtered_df_price'] = df[(df['price_paid'] >= min_price) & (df['price_paid'] <= max_price)]
        filtered_df = st.session_state['filtered_df_price']
        if not filtered_df.empty:
            display_filtered_data(filtered_df)
        else:
            st.write("No results found for the selected price range.")

propertypulse()
