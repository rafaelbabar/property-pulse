import streamlit as st
import pandas as pd
#OneDrive\Desktop\Projects\Pages>streamlit run Pugh & Co.py

import requests
from bs4 import BeautifulSoup
import html

st.title("Auction - Pugh and Co")
subheader("Online Auction Property Auction | October - 15th - 16th October 2024")
subheader("Bidding opens Tuesday 15th October 10:00 AM")

url = "https://www.pugh-auctions.com/auction/698"

response = requests.get(url)
content = BeautifulSoup(response.content, "html.parser")

props = content.find_all("div", class_="h-full mb-8")

props_file = []
base_url = "https://www.pugh-auctions.com/property/"

# List to store towns for the dropdown
towns = []

for prop in props:
    address = prop.find("div", class_="text-white group-hover:text-purple-900 uppercase text-lg font-bold flex-1 pt-3 pr-28").text.strip()
    price = prop.find("span", class_="text-xl lg:text-2xl").text.strip() if prop.find("span", class_="text-xl lg:text-2xl") else "N/A"
    price = html.unescape(price)  # Unescape HTML entities in price
    link_tag = prop.find("a", href=True)
    
    if link_tag:
        relative_link = link_tag['href']
        unique_id = relative_link.split('/')[-1]
        full_link = f"{base_url}{unique_id}/"
    else:
        full_link = "#"
    
    # Extract the town (second to last part of the address)
    address_parts = address.split(',')
    if len(address_parts) > 1:
        town = address_parts[-2].strip()
        towns.append(town)
    
    # Clean and store price for filtering
    clean_price = price.replace("£", "").replace(",", "").strip()
    price_value = int(clean_price) if clean_price.isdigit() else None
    
    props_file.append([address, town, price, price_value, full_link])

# Remove duplicates and sort the list of towns for the dropdown
towns = sorted(set(towns))

# Price range inputs with default values
st.write("Set your price range:")
min_price = st.number_input("Minimum Price", min_value=1, value=1)
max_price = st.number_input("Maximum Price", min_value=1, value=100000000)

# Create a dropdown for towns
selected_town = st.selectbox("Select a town to filter properties", towns)

# Add an "Apply Filter" button
apply_filter = st.button("Apply Filter")

if apply_filter:
    # Filter properties based on the selected town
    filtered_props = [prop for prop in props_file if prop[1] == selected_town]

    # Further filter by price range
    filtered_props = [prop for prop in filtered_props if (prop[3] is not None and min_price <= prop[3] <= max_price) or prop[3] is None]

    # Sort results: properties with valid prices first, then "N/A"
    filtered_props.sort(key=lambda x: (x[3] is None, x[3]))

    # Display the filtered properties
    if filtered_props:
        for prop in filtered_props:
            st.success(prop[0])  # Address
            st.write(f"Price: {prop[2]}")  # Price
            if prop[4] != "#":
                st.markdown(f"[Link to Property]({prop[4]})", unsafe_allow_html=True)
    else:
        st.write("No properties found for the selected filters.")

generate = st.button("Click here to save auctions")
# Option to save the filtered data
if generate and apply_filter:
    df = pd.DataFrame(filtered_props, columns=["Address", "Town", "Price", "Price Value", "Link"])
    df.to_csv("prop-po.csv", index=False, encoding="cp1252")
