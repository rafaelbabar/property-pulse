#OneDrive\Desktop\Projects\main\pages>streamlit run "Auction House.py"

import streamlit as st
import json
import os

def load_data():
    # Construct the full path to the JSON file
    json_path = os.path.join(current_dir, 'scrapers', 'auction_results.json')  # Update to use the correct JSON file

    # Load the JSON data
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def extract_unique_towns(data):
    towns = {item['town'] for item in data}
    return sorted(towns)

def parse_min_bid(min_bid):
    min_bid_value = ''.join(filter(str.isdigit, min_bid))
    return float(min_bid_value) if min_bid_value else None

# Load data when the script runs
data = load_data()

# Extract unique towns from the data
towns = extract_unique_towns(data)

# Streamlit UI components
st.title('Auction House Data')

# Filter by town
selected_town = st.selectbox('Select a town', ['All'] + towns)

# Find the price range in the dataset
all_prices = [parse_min_bid(item['price']) for item in data if parse_min_bid(item['price']) is not None]
min_price = min(all_prices) if all_prices else 0
max_price = max(all_prices) if all_prices else 1000000

# Price filter using number inputs for min and max prices
min_selected_price = st.number_input('Minimum Price (£)', min_value=min_price, max_value=max_price, value=min_price)
max_selected_price = st.number_input('Maximum Price (£)', min_value=min_price, max_value=max_price, value=max_price)

# "Apply Filters" button
if st.button('Apply Filters'):
    # Filter the data based on the selected town and price range
    filtered_data = [
        item for item in data
        if (selected_town == 'All' or item['town'] == selected_town) and
           (min_selected_price <= parse_min_bid(item['price']) <= max_selected_price)
    ]

    # Display the filtered data
    for item in filtered_data:
        address = item["address"]
        town = item["town"]
        min_bid = item["price"]
        link = item.get("link")
        
        st.write(f"**Address**: {address}")
        st.write(f"**Town**: {town}")
        st.write(f"**Price**: {min_bid}")
        st.write(f"[View Property]({link})")
        st.write("---")




