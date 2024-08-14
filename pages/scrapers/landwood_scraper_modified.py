#OneDrive\Desktop\Projects\main\pages\scrapers>python landwood_scraper_modified.py
from playwright.sync_api import sync_playwright
import json

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
            address_text = address.inner_text().strip()
            price_text = price.inner_text().strip()

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

            # Create a dictionary for each entry
            structured_data.append({
                "Address": address_text,
                "Result": result,
                "Minimum Opening Bid": min_bid
            })

        # Close the browser
        browser.close()

        # Output structured JSON data
        return json.dumps(structured_data, indent=4)

# Example of how to use the function
if __name__ == "__main__":
    data = fetch_data()
    with open('output.json', 'w') as f:
        f.write(data)
    print(data)

#with open('output.json', 'w', encoding='utf-8') as f:
    #json.dump(structured_data, f, ensure_ascii=False, indent=4)

