import json

# Define your old and new URLs
old_url = ""
new_url = ""

# Define the path to your JSON file
json_file_path = 'path/to/your/json/file.json'

# Read the JSON file
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# A recursive function to replace all occurrences of the old URL with the new one
def update_urls(obj):
    if isinstance(obj, str):
        return obj.replace(old_url, new_url)
    elif isinstance(obj, dict):
        for key in obj:
            obj[key] = update_urls(obj[key])
    elif isinstance(obj, list):
        for index, item in enumerate(obj):
            obj[index] = update_urls(item)
    return obj

# Update all URLs in the JSON data
updated_data = update_urls(data)

# Write the updated JSON data back to the file
with open(json_file_path, 'w', encoding='utf-8') as file:
    json.dump(updated_data, file, ensure_ascii=False, indent=4)

print(f"Updated URLs in {json_file_path}")
