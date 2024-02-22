import requests
import json
import os

url = 'https://scrapeninja.p.rapidapi.com/scrape'

# get your subscription key at https://rapidapi.com/restyler/api/scrapeninja from "Code generator",
# copy&paste it to 'x-rapidapi-key' header below

headers =     {
    "Content-Type": "application/json",
    "x-rapidapi-host": "scrapeninja.p.rapidapi.com",
    "x-rapidapi-key": "YOUR_RAPID"
    }

payload =        {
    "url": "imput your url here",
    "device": "desktop",
    "adblock": "false",
    "country": "US",
    "language": "en"
    
       }

# Make the POST request
response = requests.request("POST", url, json=payload, headers=headers)

# The response content
response_json = response.json()

# The file path where you want to save the response JSON
# Note that in this environment, you have to save to the /mnt/data/ directory.
file_path = ''

# Writing the response to a JSON file
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(response_json, f, ensure_ascii=False, indent=4)

# Provide the path for the user to know where the file is saved
print(f"Response JSON has been saved to {file_path}")
