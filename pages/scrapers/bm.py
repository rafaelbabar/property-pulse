#OneDrive\Desktop\Projects\main\pages\scrapers>python bm.py

from playwright.sync_api import sync_playwright
import json

def fetch_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Run in non-headless mode
        page = browser.new_page()

        try:
            page.goto("https://www.barnardmarcusauctions.co.uk/auctions/12-september-2024/", timeout=60000)  # 60 seconds timeout
            page.wait_for_timeout(10000)  # Wait 10 seconds for JavaScript to load completely

            # Extract addresses, locations, prices, and property links
            addresses = page.query_selector_all('div.lot-item__address') if page.query_selector('div.lot-item__address') else []
            locations = page.query_selector_all('div.lot-item__location') if page.query_selector('div.lot-item__location') else []
            prices = page.query_selector_all('strong') if page.query_selector('strong') else []

            # Filter to include only those that make sense as prices (e.g., containing "£" or certain numbers)
            filtered_prices = [price for price in prices if "£" in price.inner_text() or price.inner_text().isdigit()]
            links = page.query_selector_all('a')

            # Filter links to include only those relevant to property listings
            filtered_links = [link for link in links if link.get_attribute('href') and link.get_attribute('href').startswith('https://www.barnardmarcusauctions.co.uk/auctions/')]

            # Debug output
            print(f"Found {len(addresses)} addresses")
            print(f"Found {len(locations)} locations")
            print(f"Found {len(prices)} prices")
            print(f"Found {len(links)} links")
            print(f"Filtered to {len(filtered_links)} relevant links")

            # List to hold structured data
            structured_data = []

            for address, location, price, link in zip(addresses, locations, filtered_prices, filtered_links):
                # Clean up the address, location, and price strings
                address_text = address.inner_text().strip().replace("\u00a0", " ")
                location_text = location.inner_text().strip().replace("\u00a0", " ")
                price_text = price.inner_text().strip().replace("\u00a3", "£")
                link_href = link.get_attribute('href')  # Directly use the href attribute

                # Debug output for each entry
                print(f"Address: {address_text}, Location: {location_text}, Price: {price_text}, Link: {link_href}")

                # Extract the town from the location
                town = location_text.split(",")[0]  # Assuming town is the first part of the location

                # Determine the result and minimum bid from the price_text
                if "Sold for" in price_text:
                    result = "Sold"
                    min_bid = price_text.split("for ")[-1]
                else:
                    result = "Available"
                    min_bid = price_text

                # Append the structured data with the link
                structured_data.append({
                    "Address": address_text,
                    "Location": location_text,
                    "Town": town,
                    "Result": result,
                    "Minimum Opening Bid": min_bid,
                    "Link": link_href  # Include the full property link
                })
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            browser.close()
            return structured_data

if __name__ == "__main__":
    data = fetch_data()
    # Save the data to a JSON file
    if data:
        with open('bm.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    else:
        print("No data was scraped.")





