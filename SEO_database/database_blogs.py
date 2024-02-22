import sqlite3
import csv
import json
import requests
from bs4 import BeautifulSoup

# Step 1: SQLite Database Setup
db_file_path = 'C://Users//luizm//webscraper//blog para casa//seo_data.db'
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS seo_data (
        id INTEGER PRIMARY KEY,
        url TEXT,
        title TEXT,
        meta_description TEXT,
        first_h1 TEXT,
        first_link TEXT,
        first_image TEXT,
        body_text TEXT
    )
''')
conn.commit()

# Function to insert data into the database
def insert_seo_data(data):
    try:
        with sqlite3.connect(db_file_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO seo_data (url, title, meta_description, first_h1, first_link, first_image, body_text)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (data['url'], data['title'], data['meta_description'], data['first_h1'], data['first_link'], data['first_image'], data['body_text']))
            conn.commit()
    except sqlite3.Error as error:
        print("Error occurred while inserting data into the database:", error)

# Step 2: SEO Data Extraction
headers = {
    "Content-Type": "application/json",
    "x-rapidapi-host": "scrapeninja.p.rapidapi.com",
    "x-rapidapi-key": "3803388fe2mshb80313878a812c7p1db98bjsn12a17760f57c"  # Replace with your actual API key
}
json_file_path = 'C://Users//luizm//webscraper//blog para casa//urls.json'
try:
    with open(json_file_path, 'r', encoding='utf-8') as file:
        urls = json.load(file)
except FileNotFoundError:
    print("Error: JSON file not found")
    urls = []

# Iterate over each URL and extract data
for url in urls:
    payload = {"url": url}
    try:
        response = requests.post('https://scrapeninja.p.rapidapi.com/scrape', json=payload, headers=headers)
        response_json = response.json()
        soup = BeautifulSoup(response_json['body'], 'html.parser')

        # Extract the body text for analysis
        body_text = soup.get_text(separator=' ', strip=True)

        seo_data = {
            'url': url,
            'title': soup.title.string if soup.title else 'No title',
            'meta_description': next((meta.get('content', '') for meta in soup.find_all('meta') if meta.get('name') == 'description'), 'No meta description'),
            'first_h1': next((h1.get_text(strip=True) for h1 in soup.find_all('h1')), 'No H1'),
            'first_link': next((link['href'] for link in soup.find_all('a', href=True)), 'No links'),
            'first_image': next((img.get('src', 'No src attribute') for img in soup.find_all('img')), 'No images'),
            'body_text': body_text
        }

        # Step 3: Data Insertion
        insert_seo_data(seo_data)
    except (requests.RequestException, ValueError, IndexError, AttributeError) as e:
        print(f"Error occurred while processing {url}: {str(e)}")

print(f"SEO data extraction and insertion completed.")
