#OneDrive\Desktop\Projects\main\pages\scrapers>python landwood_scraper_modified_with_links.py


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
        browser = p.chromium.launch(headless=False)  # Run in non-headless mode
        page = browser.new_page()

        try:
            page.goto("https://www.landwoodpropertyauctions.com/future-auctions?showall=true", timeout=60000)  # 60 seconds timeout
            page.wait_for_timeout(10000)  # Wait 10 seconds for JavaScript to load completely

            # Example: Extract addresses, prices, and property links
            addresses = page.query_selector_all('h3.list-address.primary-text') if page.query_selector('h3.list-address.primary-text') else []
            prices = page.query_selector_all('h4 strong') if page.query_selector('h4 strong') else []
            links = page.query_selector_all('a.btn.btn-success')  # Specifically target the 'a' tags with the class 'btn btn-success'

            # Debug output
            print(f"Found {len(addresses)} addresses")
            print(f"Found {len(prices)} prices")
            print(f"Found {len(links)} links")

            # List to hold structured data
            structured_data = []

            base_url = "https://www.landwoodpropertyauctions.com/"

            for address, price, link in zip(addresses, prices, links):
                # Clean up the address and price strings
                address_text = address.inner_text().strip().replace("\u00a0", " ")
                price_text = price.inner_text().strip().replace("\u00a3", "£")
                link_href = base_url + link.get_attribute('href')  # Prepend the base URL to the link

                # Debug output for each entry
                print(f"Address: {address_text}, Price: {price_text}, Link: {link_href}")

                # Extract the town from the address
                town = extract_town_from_address(address_text)

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
        with open('output_with_full_links.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    else:
        print("No data was scraped.")



