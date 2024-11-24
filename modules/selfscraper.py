import os
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from pathlib import Path

# from settings import YOUR_RAPIDAPI_KEY

# Scrapeninja configuration
API_URL = 'https://scrapeninja.p.rapidapi.com/scrape'
HEADERS = {
    "Content-Type": "application/json",
    "x-rapidapi-host": "scrapeninja.p.rapidapi.com",
    "x-rapidapi-key": "3803388fe2mshb80313878a812c7p1db98bjsn12a17760f57c",  # Replace with your actual API key
}


# Payload configuration
payload = {
    "url": "https://casaconfortoblog.wordpress.com/",
    "headers": [
        "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    ]
}

# Request the page content
response = requests.post(API_URL, json=payload, headers=HEADERS)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract information
    extracted_data = {
        'title': soup.title.string if soup.title else "No title found",
        'meta_description': soup.find('meta', attrs={'name': 'description'}).get('content') if soup.find('meta', attrs={'name': 'description'}) else "No description found",
        'links': [
            {'href': link['href'], 'text': link.get_text(strip=True)}
            for link in soup.find_all('a', href=True)
        ]
    }

    # Save to JSON
    output_dir = Path("output/blog_posts")
    output_dir.mkdir(parents=True, exist_ok=True)
    json_file_path = output_dir / "extracted_data.json"

    with open(json_file_path, 'w', encoding='utf-8') as f:
        json.dump(extracted_data, f, ensure_ascii=False, indent=4)

    print(f"Extracted data saved to {json_file_path}")

    # Save links to CSV
    links_df = pd.DataFrame(extracted_data['links'])
    links_csv_path = output_dir / "extracted_links.csv"
    links_df.to_csv(links_csv_path, index=False, encoding='utf-8')

    print(f"Links saved to {links_csv_path}")

else:
    print(f"Failed to scrape the website. Status code: {response.status_code}")
    print(f"Error message: {response.text}")