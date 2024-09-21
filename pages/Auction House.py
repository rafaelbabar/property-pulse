#OneDrive\Desktop\Projects\main\pages\scrapers>python auction-house-1.py
from playwright.sync_api import sync_playwright
import json
import time
import os

def extract_town_from_address(address):
    address = address.replace("\\u00a0", " ")
    address_parts = address.split(',')
    postcode = address_parts[-1].strip()
    if len(address_parts) >= 2:
        town = address_parts[-2].strip()
    else:
        town = address_parts[0].strip()
    return town

def fetch_data():
    base_url = "https://www.auctionhouse.co.uk"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            page.goto(f"{base_url}/online/auction/2024/9/24", timeout=60000)
            time.sleep(5)

            # Now we target 'summary-info-wrapper' to extract property details
            properties = page.query_selector_all("a.home-lot-wrapper-link")
            
            results = []
            for property in properties:
                # Extract the link from the <a> tag
                relative_link = property.get_attribute("href").strip()
                full_link = relative_link if relative_link else "N/A"
                
                # Extract the property type (first <p> tag in summary-info-wrapper)
                property_type = property.query_selector("div.summary-info-wrapper p").inner_text().strip()
                
                # Extract the full address (second <p> tag in summary-info-wrapper)
                address = property.query_selector_all("div.summary-info-wrapper p")[1].inner_text().strip()
                
                # Extract the town from the address
                town = extract_town_from_address(address)
                
                # Debugging the elements before extracting price and link
                print(f"Property Type: {property_type}, Address: {address}, Link: {full_link}")
                
                # Extract the price from the correct div
                price_tag = property.query_selector("div.lotbg-online.text-white.grid-view-guide")
                if price_tag:
                    price = price_tag.inner_text().strip().replace("*Guide | ", "").replace("\\u00a3", "£").replace("+", "").strip()
                    print(f"Found Price: {price}")
                else:
                    price = "N/A"
                    print("Price not found.")
                
                results.append({
                    "property_type": property_type,
                    "address": address,
                    "town": town,
                    "price": price,
                    "link": full_link
                })

            # Define the path where the JSON file will be saved
            output_file_path = os.path.expanduser('D:/OneDrive/Desktop/Projects/main/pages/scrapers/auction_results.json')

            # Save the results to a JSON file
            with open(output_file_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=4)

            print(f"Results saved to {output_file_path}")
            print(json.dumps(results, indent=4, ensure_ascii=False))

        finally:
            browser.close()

fetch_data()




