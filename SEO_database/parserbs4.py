import sqlite3
import requests
import random
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
import re
from collections import Counter
from nltk.corpus import stopwords
from nltk.util import ngrams
import nltk
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import SEARCH_ENGINE_ID, setup_logger, GOOGLE_API_KEY
# Add paths to sys.path for importing modules from different directories
from scraper.google_search import BLOCK_LIST, get_main_page_url, perform_google_search  # Assuming this is the correct function name

# Download NLTK Portuguese stopwords
nltk.download('stopwords')

# Database file path
db_file_path = 'C://Users//luizm//webscraper//blog para casa//seo_data.db'

# Connect to the SQLite database
conn = sqlite3.connect(db_file_path)
cursor = conn.cursor()

# Query to fetch relevant fields from the database
cursor.execute("SELECT title, meta_description, first_h1 FROM seo_data")
rows = cursor.fetchall()

# Initialize an empty string to aggregate text
aggregated_text = ''

# Aggregate relevant text from each row
for row in rows:
    aggregated_text += ' '.join([str(field) for field in row if field])

def perform_google_search(query, start_index=1, num_results=10):  # noqa: F811
    logger = setup_logger('search_logger', 'google_search.log')
    logger.info(f"Performing search for query: {query}")

    results = []
    total_results_fetched = 0
    url = 'https://www.googleapis.com/customsearch/v1'
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        # Add more user agents here if needed
    ]

    with requests.Session() as session:
        while total_results_fetched < num_results:
            headers = {
                'User-Agent': random.choice(user_agents)
            }
            params = {
                'q': f"{query} {BLOCK_LIST}",
                'key': GOOGLE_API_KEY,
                'cx': SEARCH_ENGINE_ID,
                'start': start_index,
                'gl': 'br',  # Geolocation set to Brazil
                'lr': 'lang_pt',  # Language restrict to Portuguese
            }

            try:
                response = session.get(url, headers=headers, params=params)
                response.raise_for_status()
                search_data = response.json()
                search_results = search_data.get('items', [])

                cache = {}  # Define the cache variable

                for item in search_results:
                    page_url = get_main_page_url(item['link'])
                    if page_url not in cache:  # Check if URL is not in cache
                        results.append({
                            'link': page_url,
                            'title': item.get('title'),
                            'snippet': item.get('snippet')
                        })
                        cache[page_url] = True  # Add URL to cache
                        total_results_fetched += 1
                        if total_results_fetched == num_results:
                            break

                start_index += len(search_results)

            except (HTTPError, ConnectionError, Timeout, RequestException) as err:
                logger.error(f"Error during Google Search: {err}")
                break

    return results

    

# Function to clean and tokenize text
def tokenize(text):
    # Remove non-alphanumeric characters
    text = re.sub(r'\W+', ' ', text.lower())
    # Tokenize
    tokens = text.split()
    # Remove Portuguese stopwords
    stop_words = set(stopwords.words('portuguese'))
    tokens = [word for word in tokens if word not in stop_words and len(word) > 1]
    return tokens

# Tokenize the aggregated text
tokens = tokenize(aggregated_text)

# Extract bi-grams and tri-grams
bigrams = [' '.join(grams) for grams in ngrams(tokens, 2)]
trigrams = [' '.join(grams) for grams in ngrams(tokens, 3)]

# Combine single words, bi-grams, and tri-grams
all_keywords = tokens + bigrams + trigrams

# Count the frequency of each keyword/phrase
word_freq = Counter(all_keywords)

# Get the top keywords/phrase with frequencies
top_keywords_with_freq = word_freq.most_common(30)

# File to save the results
results_file_path = 'C://Users//luizm//webscraper//blog para casa//search_results.json'

# Save results to a file
with open(results_file_path, 'w', encoding='utf-8') as file:
    for keyword, freq in top_keywords_with_freq:
        results = perform_google_search(keyword, 10)
        print(f"Saving results for '{keyword}'")
        file.write(json.dumps({keyword: results}, indent=2))
        file.write('\n')  # Newline for separation between keywords

print(f"Search results saved to {results_file_path}")

# Close the database connection
conn.close()