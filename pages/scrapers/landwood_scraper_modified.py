#OneDrive\Desktop\Projects\main\pages\scrapers>python landwood_scraper_modified.py
from playwright.sync_api import sync_playwright
import json

def extract_town_from_address(address):
    # Clean up any non-breaking spaces first
    address = address.replace("\u00a0", " ")

    # Split the address by commas
    address_parts = address.split(',')
    
    # The last part is assumed to be the postcode
    postcode = address_parts[-1].strip()
    
    # The second last part is assumed to be the town
    if len(address_parts) >= 2:
        town = address_parts[-2].strip()
    else:
        # Fallback: if the address doesn't have enough parts, return the first part
        town = address_parts[0].strip()
    
    return town

def fetch_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.landwoodpropertyauctions.com/future-auctions?showall=true")  # Replace with your target URL
        page.wait_for_timeout(5000)  # Wait for JavaScript to load

        # Example: Extract addresses and prices
        addresses = page.query_selector_all('h3.list-address.primary-text') if page.query_selector('h3.list-address.primary-text') else []
        prices = page.query_selector_all('h4 strong') if page.query_selector('h4 strong') else []

        # List to hold structured data
        structured_data = []

        for address, price in zip(addresses, prices):
            # Clean up the address and price strings
            address_text = address.inner_text().strip().replace("\u00a0", " ")
            price_text = price.inner_text().strip().replace("\u00a3", "£")
            
            # Extract the town from the address
            town = extract_town_from_address(address_text)

            # Determine the result and minimum bid from the price_text
            if "Sold for" in price_text:
                result = "Sold"
                min_bid = price_text.split("for ")[-1]
            elif "Sold Prior" in price_text:
                result = "Sold Prior"
                min_bid = "N/A"
            elif "Withdrawn" in price_text:
                result = "Withdrawn"
                min_bid = "N/A"
            elif "Unsold" in price_text:
                result = "Unsold"
                min_bid = "N/A"
            elif "Postponed" in price_text:
                result = "Postponed"
                min_bid = "N/A"
            else:
                result = "Minimum Opening Bid"
                min_bid = price_text

            # Create a dictionary for each entry including the town
            structured_data.append({
                "Address": address_text,
                "Town": town,
                "Result": result,
                "Minimum Opening Bid": min_bid
            })

        # Close the browser
        browser.close()

        # Output structured JSON data
        return json.dumps(structured_data, ensure_ascii=False, indent=4)

# Example of how to use the function
if __name__ == "__main__":
    data = fetch_data()
    with open('output.json', 'w', encoding='utf-8') as f:
        f.write(data)
    print(data)




