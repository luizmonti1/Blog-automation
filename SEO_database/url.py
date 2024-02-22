import json

# File path for the input JSON file
input_json_file_path = 'c://Users//luizm//webscraper//blog para casa//resultados.json'

# File path for the output JSON file
output_json_file_path = 'C:/Users/luizm/webscraper/blog para casa/urls.json'

# Read the JSON file
with open(input_json_file_path, 'r') as file:
    data = json.load(file)

# List to store extracted URLs
urls = []

# Check if data is a list
if isinstance(data, list):
    # Loop through each item in the list
    for item in data:
        # Extract the URL from each item and add to the list
        url = item.get('url', 'URL not found')
        urls.append(url)
else:
    # If data is not a list, extract the URL directly from the dictionary
    url = data.get('url', 'URL not found')
    urls.append(url)

# Save the URLs to the output file
with open(output_json_file_path, 'w', encoding='utf-8') as file:
    json.dump(urls, file, indent=4)

print(f"URLs saved to {output_json_file_path}")
