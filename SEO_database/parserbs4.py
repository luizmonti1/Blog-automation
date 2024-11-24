import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin
from collections import Counter
from nltk.corpus import stopwords
from nltk import download as nltk_download, word_tokenize, ngrams
import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("optimized_scraper")

# Download NLTK data
nltk_download('stopwords')
nltk_download('punkt')

# User-Agent rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
]

HEADERS = {"User-Agent": USER_AGENTS[0]}

# Database connection setup
DB_FILE_PATH = "E:\Apps\Blog-automation-main\data\seo_data.db"

def connect_to_database(db_file_path):
    """Establish a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(db_file_path)
        logger.info("Connected to the database successfully.")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection failed: {e}")
        return None

def fetch_page(url):
    """Fetch the HTML content of a given URL."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return None

def parse_metadata(soup):
    """Extract metadata from the page."""
    metadata = {
        "title": soup.title.string if soup.title else "No title found",
        "description": (
            soup.find("meta", attrs={"name": "description"}) or
            soup.find("meta", attrs={"property": "og:description"})
        ),
        "canonical": soup.find("link", rel="canonical"),
    }
    # Extract values
    for key, value in metadata.items():
        if value and hasattr(value, "get"):
            metadata[key] = value.get("content", "No content found")
    return metadata

def parse_content(soup):
    """Extract the main content using <article> or heuristics."""
    article = soup.find("article")
    if article:
        return article.get_text(strip=True)
    # Fallback: find the largest block of text
    paragraphs = soup.find_all("p")
    return max(paragraphs, key=lambda p: len(p.get_text()), default="").get_text(strip=True)

def extract_links(soup, base_url):
    """Extract and resolve all valid links on the page."""
    links = []
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        full_url = urljoin(base_url, href)
        links.append(full_url)
    return list(set(links))  # Remove duplicates

def tokenize_and_extract_keywords(text):
    """Tokenize text and extract significant keywords."""
    text = re.sub(r'\W+', ' ', text.lower())
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words("portuguese") + stopwords.words("english"))
    filtered_tokens = [word for word in tokens if word not in stop_words and len(word) > 2]
    bigrams = [' '.join(gram) for gram in ngrams(filtered_tokens, 2)]
    trigrams = [' '.join(gram) for gram in ngrams(filtered_tokens, 3)]
    return Counter(filtered_tokens + bigrams + trigrams).most_common(20)

def scrape(url):
    """Main scraper function."""
    logger.info(f"Scraping {url}")
    html = fetch_page(url)
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")

    # Parse metadata
    metadata = parse_metadata(soup)

    # Parse main content
    main_content = parse_content(soup)

    # Extract links
    links = extract_links(soup, url)

    # Analyze keywords
    keywords = tokenize_and_extract_keywords(main_content)

    # Compile results
    return {
        "url": url,
        "metadata": metadata,
        "content": main_content[:500],  # Limit content preview
        "keywords": keywords,
        "links": links[:10]  # Limit the number of links
    }

def fetch_and_save_results():
    """Fetch data from the database and perform scraping."""
    conn = connect_to_database(DB_FILE_PATH)
    if not conn:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT title, meta_description, first_h1 FROM seo_data")
        rows = cursor.fetchall()

        aggregated_text = ' '.join(
            ' '.join(map(str, row)) for row in rows if row
        )

        # Tokenize aggregated text and extract keywords
        tokens = tokenize_and_extract_keywords(aggregated_text)

        # File to save the results
        results_file_path = "search_results.json"

        # Save results to a file
        with open(results_file_path, 'w', encoding='utf-8') as file:
            for keyword, freq in tokens:
                results = scrape(f"https://www.google.com/search?q={keyword}")
                if results:
                    logger.info(f"Saving results for '{keyword}'")
                    file.write(json.dumps({keyword: results}, ensure_ascii=False, indent=4))
                    file.write('\n')  # Newline for separation between keywords

        logger.info(f"Search results saved to {results_file_path}")

    except sqlite3.Error as e:
        logger.error(f"Database query failed: {e}")

    finally:
        conn.close()

if __name__ == "__main__":
    fetch_and_save_results()
