#OneDrive\Desktop\Projects\main\pages>streamlit run Landwood.py
import streamlit as st
import json
import os

def load_data():
    # Get the directory where the current script is located
    current_dir = os.path.dirname(__file__)
    
    # Construct the full path to the JSON file
    json_path = os.path.join(current_dir, 'scrapers', 'output.json')
    
    # Load the JSON data
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_unique_towns(data):
    # Extract unique towns from the loaded data
    towns = {item['Town'] for item in data}
    return sorted(towns)

def parse_min_bid(min_bid):
    # Try to extract a numeric value from min_bid, otherwise return None
    try:
        if "£" in min_bid:
            return int(min_bid.replace("£", "").replace(",", "").strip())
        else:
            return None
    except ValueError:
        return None

# Load the data
data = load_data()

# Extract unique towns from the data
towns = extract_unique_towns(data)

st.title("Auction - Landwood")

# Search by town using a dropdown menu
town_search = st.selectbox("Select a Town", options=["All"] + towns)

# Search by price range
min_price = st.number_input("Minimum Price (£)", min_value=0, value=0)
max_price = st.number_input("Maximum Price (£)", min_value=0, value=1000000)

# Apply Filters button
if st.button("Apply Filters"):
    st.subheader("Filtered Auction Properties and Details")
    for item in data:
        address = item["Address"]
        town = item["Town"]
        result = item["Result"]
        min_bid = item["Minimum Opening Bid"]

        # Parse the numeric value from the minimum opening bid
        min_bid_value = parse_min_bid(min_bid)

        # Filter by town and price
        if min_bid_value is not None and (town_search == "All" or town_search == town) and (min_price <= min_bid_value <= max_price):
            st.write(f"**Address:** {address}")
            st.write(f"**Town:** {town}")
            st.write(f"**Result:** {result}")
            st.write(f"**Minimum Opening Bid:** £{min_bid_value:,}")
            st.write("---")  # Add a line for better visual separation
