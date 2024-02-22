# Python Backend for Blog Content Automation

## Overview

This Python backend automates content creation for blog posts by performing custom searches on Google with specific keywords related to the blog's topics. It extracts documentation from relevant websites, parses the data, and implements logic to identify the top 30 keywords among other criteria. Furthermore, it includes a data parser for Amazon, filtering best sellers and automatically generating a sheet with essential product information, including image links, affiliate links, ratings, number of reviews, and prices. This system ensures the blog always features the best links for its audience, enhancing both content quality and user engagement.

## Features

- **Custom Google Search**: Automates searches for blog-related topics to find relevant websites.
- **Data Extraction and Parsing**: Extracts and parses website content to identify valuable information and keywords.
- **Amazon Data Parser**: Filters Amazon best sellers, extracting product details for blog content.
- **Automated Affiliate Link Generation**: Creates affiliated links for products to be featured in blog posts.
- **Content Optimization**: Uses logic to determine top keywords and best products based on ratings, reviews, and prices.

## Getting Started

### Prerequisites

- Python 3.8+
- BeautifulSoup4 for HTML parsing
- Requests for making HTTP requests
- pandas for data manipulation
- Google Custom Search JSON API credentials
- Amazon Product Advertising API credentials

### Installation

Clone the repository:

```bash
git clone https://yourrepositorylink.git
cd your-project-directory
```

Install the required packages:

```bash
pip install -r requirements.txt
```

### Usage

1. **Setting Up API Credentials**:

   - Place your Google Custom Search and Amazon Product Advertising API credentials in `credentials.json`.

2. **Running the Custom Google Search**:

   ```python
   python custom_google_search.py
   ```

   - Customize your search queries in `search_queries.txt`.

3. **Executing the Amazon Data Parser**:
   ```python
   python amazon_data_parser.py
   ```
   - The script will generate a `products.csv` file with all the necessary product information.

## How It Works

- **Custom Google Search**: The system uses predefined keywords to perform searches and extract the top websites for content inspiration.
- **Data Extraction and Parsing**: It analyzes the fetched documents, extracting essential data and computing the top keywords for SEO optimization.
- **Amazon Data Parser**: By accessing the Amazon Product Advertising API, it retrieves detailed information about best-selling products, automating the creation of affiliate links and selecting the best products based on defined criteria.
