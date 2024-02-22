import sqlite3
import re
from collections import Counter
from nltk.corpus import stopwords
import nltk
import csv

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

# Count the frequency of each word
word_freq = Counter(tokens)

# Get the 30 most common words
top_30_keywords = word_freq.most_common(30)

# File path for saving the keywords
keywords_file_path = 'C://Users//luizm//webscraper//blog para casa//top_keywords.csv'

# Write the keywords to a CSV file
with open(keywords_file_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Keyword', 'Frequency'])

    for word, freq in top_30_keywords:
        writer.writerow([word, freq])

print(f"Top 30 keywords saved to {keywords_file_path}")

# Close the database connection
conn.close()
