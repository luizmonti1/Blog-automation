import os
import json
import sys
from pathlib import Path

# Add the project root to PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

from config.settings import BASE_DIR, JSON_FILE_PATH, OLD_URL, NEW_URL

# A recursive function to replace all occurrences of the old URL with the new one
def update_urls(obj, old_url, new_url):
    if isinstance(obj, str):
        return obj.replace(old_url, new_url)
    elif isinstance(obj, dict):
        for key in obj:
            obj[key] = update_urls(obj[key], old_url, new_url)
    elif isinstance(obj, list):
        for index, item in enumerate(obj):
            obj[index] = update_urls(item, old_url, new_url)
    return obj

# Ensure the JSON file path exists
if not JSON_FILE_PATH.exists():
    print(f"Error: File not found at {JSON_FILE_PATH}")
    exit(1)

# Read the JSON file
try:
    with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Update all URLs in the JSON data
    updated_data = update_urls(data, OLD_URL, NEW_URL)

    # Write the updated JSON data back to the file
    with open(JSON_FILE_PATH, 'w', encoding='utf-8') as file:
        json.dump(updated_data, file, ensure_ascii=False, indent=4)

    print(f"Updated URLs in {JSON_FILE_PATH}")

except json.JSONDecodeError:
    print(f"Error: Invalid JSON format in {JSON_FILE_PATH}")

if not OLD_URL or not NEW_URL:
    print("Error: OLD_URL and NEW_URL must be set in settings.py")
    exit(1)
