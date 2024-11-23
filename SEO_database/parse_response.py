import json
import csv

def parse_response(html):
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html, 'html.parser')
    
    meta_tags = soup.find_all('meta', attrs={'name': 'description'})  # Find all meta tags with name='description'
    meta_description = meta_tags[0]['content'] if meta_tags else ''
    
    h1_tags = soup.find_all('h1')  # Find all h1 tags
    first_h1 = h1_tags[0].text if h1_tags else ''
    
    response_json = {
        'meta_description': meta_description,
        'first_h1': first_h1
    }
    
    return response_json

def save_results(response_json, file):
    with open(file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=response_json.keys())
        writer.writeheader()
        writer.writerow(response_json)

def main():
    source = "C:\\Users\\luizm\\webscraper\\blog para casa\\response_json.json"

    with open(source, 'r') as f:
        data = json.load(f)

    # Access the parsed data
    meta_description = data.get('meta_description', '')
    first_h1 = data.get('first_h1', '')

    # Use the parsed data as needed
    print(meta_description)
    print(first_h1)

    with open('response.html', 'r', encoding='utf-8') as f:
        response_html = f.read()
    
    response_json = parse_response(response_html)
    save_results(response_json, 'response.csv')