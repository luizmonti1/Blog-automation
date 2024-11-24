from bs4 import BeautifulSoup
import pandas as pd

def get_amazon_best_sellers(file_path):
    try:
        # Read the HTML content from the file
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

        # Initialize a list to store product data
        products = []

        # Iterate over each product and extract details
        for product in soup.select('#gridItemRoot'):
            # Extract product title
            title_element = product.select_one('div._cDEzb_p13n-sc-css-line-clamp-3_g3dy1')
            title = title_element.text.strip() if title_element else 'N/A'

            # Extract product image URL
            image_element = product.select_one('img.a-dynamic-image')
            image_url = image_element['src'] if image_element else 'N/A'

            # Extract product rating
            rating_element = product.select_one('a.a-link-normal[title]')
            rating = rating_element['title'].strip() if rating_element else 'N/A'

            # Extract number of reviews
            num_reviews_element = product.select_one('i.a-icon-star-small + span')
            num_reviews = num_reviews_element.text.strip() if num_reviews_element else 'N/A'

            # Extract product price
            price_element = product.select_one('span._cDEzb_p13n-sc-price_3mJ9Z')
            price = price_element.text.strip() if price_element else 'N/A'

            # Append the product data to the list
            products.append({
                'Title': title,
                'Image URL': image_url,
                'Rating': rating,
                'Number of Reviews': num_reviews,
                'Price': price
            })

        # Create a DataFrame from the product list
        return pd.DataFrame(products)

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Local HTML file path
file_path = "C:\\Users\\luizm\\webscraper\\produtos_amazon\\Amazon.com.br Mais Vendidos_ Mouses de Computador - os mais vendidos na Amazon.com.br.html"

# Get the best sellers data
df = get_amazon_best_sellers(file_path)

# Check if the DataFrame is not None and not empty
if df is not None and not df.empty:
    # Save the DataFrame to a CSV file
    csv_file_name = 'amazon_best_sellers.csv'
    df.to_csv(csv_file_name, index=False)
    print(f"Data saved to {csv_file_name}")
else:
    print("Failed to retrieve or parse the data from Amazon.")
