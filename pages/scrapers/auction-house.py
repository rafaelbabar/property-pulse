#OneDrive\Desktop\Projects\main\pages\scrapers>python auction-house.py
from playwright.sync_api import sync_playwright
import json
import time
import os

def extract_town_from_address(address):
    address = address.replace("\u00a0", " ")
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
            page.goto(f"{base_url}/manchester/auction/search-results", timeout=60000)
            time.sleep(5)

            properties = page.query_selector_all("p.lot-addr")

            results = []
            for property in properties:
                # Extract the street and area (excluding postcode)
                street_area = property.inner_text().strip()
                
                # Extract the postcode
                postcode_tag = property.query_selector("span.address-postcode")
                postcode = postcode_tag.inner_text().strip() if postcode_tag else ""
                
                # Combine to form the full address, avoiding duplicate postcode
                if postcode and postcode not in street_area:
                    full_address = f"{street_area} {postcode}".strip()
                else:
                    full_address = street_area.strip()
                
                # Extract the price and ensure correct encoding for £ symbol
                price_tag = property.evaluate_handle('el => el.closest("div").querySelector("span.price")')
                price = price_tag.inner_text().strip().replace("\u00a3", "£") if price_tag else "N/A"
                
                # Extract the link
                link_tag = property.evaluate_handle('el => el.closest("div").querySelector("a[href]")')
                relative_link = link_tag.get_attribute("href").strip() if link_tag else ""
                full_link = f"{base_url}{relative_link}" if relative_link else "N/A"
                
                # Extract the town from the address
                town = extract_town_from_address(full_address)

                results.append({
                    "address": full_address,
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



