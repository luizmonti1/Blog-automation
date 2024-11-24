import requests
from bs4 import BeautifulSoup
import json

# Scrapeninja configuration
url = 'https://scrapeninja.p.rapidapi.com/scrape'
headers = {
    "Content-Type": "application/json",
    "x-rapidapi-host": "scrapeninja.p.rapidapi.com",
    "x-rapidapi-key": "YOUR-RAPID"
}

payload = {
    "url": "https://casaconfortoblog.wordpress.com/",
    "headers": [
        "authority: casaconfortoblog.wordpress.com",
        "accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language: en-US,en;q=0.9,pt;q=0.8",
        "cache-control: no-cache",
        "pragma: no-cache",
        "referer: https://casaconfortoblog.wordpress.com/",
        "sec-ch-ua: \"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
        "sec-ch-ua-mobile: ?0",
        "sec-ch-ua-platform: \"Windows\"",
        "sec-fetch-dest: document",
        "sec-fetch-mode: navigate",
        "sec-fetch-site: same-origin",
        "sec-fetch-user: ?1",
        "upgrade-insecure-requests: 1",
        "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Cookie: __utma=11735858.1707176772.1704822879.1704822879.1704822879.1; __utmc=11735858; __utmz=11735858.1704822879.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); ccpa_applies=false; usprivacy=1---; _parsely_visitor={%22id%22:%22pid=b55eea50-3e5e-4f96-8a08-eb27c113183f%22%2C%22session_count%22:1%2C%22last_session_ts%22:1704837048785}; _fbp=fb.1.1704837048873.604499213; _gcl_au=1.1.909941581.1704837049; tk_ai_explat=GscYkYOQtqRbiE0Pm51ewFVC; _parsely_slot_click={%22url%22:%22https://wordpress.com/%22%2C%22x%22:1819%2C%22y%22:0%2C%22xpath%22:%22//*[@id=%5C%22wpcom-home%5C%22]/div[1]/nav[1]/ul[2]/li[1]/a[1]%22%2C%22href%22:%22https://wordpress.com/log-in/%22}; wordpress_test_cookie=WP%20Cookie%20check; recognized_logins=IyLcYter1aQQCWRZOzcfHt0yDb2StAr-_ZlmXsut4Z1iaaxXf_Tzsqn8airjs3MhL9jKm4r1wCbtOq8wjU4fKA%3D%3D; wordpress_logged_in=luizmonti1%7C1799445057%7CaAT9y1CGAM7mUkVavGQEECkr5l6EzJkTZ1WTFdtbsxJ%7Cfa53c41285e38004e11a559fa97581359dbf7a9d48a8811d4757c9ad39f87526; _wpndash=d88890108becf7e55dd62b3f; _hjSessionUser_227769=eyJpZCI6IjYzZTJlYTBiLTQxZmUtNWI1Ny05YWUyLWVhOGM1ZWE5YmY1YyIsImNyZWF0ZWQiOjE3MDQ4MzcwNDg5MzYsImV4aXN0aW5nIjp0cnVlfQ==; _gid=GA1.2.204683803.1704837061; _pin_unauth=dWlkPVpqVXpOVGxrTWprdFlqSXpNUzAwTlRoaExXSTRZbVV0Wm1JMU5EWXdORFJrTkdSaA; __ssid=d54c8502497e1b70fec9cab08583315; __stripe_mid=85bd1514-0a5b-434f-a446-cca056179ce0bcdc58; _ga=GA1.3.1807287909.1704837049; ad_details=utm_medium%3Demail%26utm_campaign%3Dwpcom-free-site-onboarding-getting-started-1%26utm_source%3Dguides; ad_timestamp=1704840219; wp-settings-time-239117472=1704850867; wp-settings-239117472=libraryContent%3Dbrowse; _uetsid=26803530af3911ee925dd5eeaa0be9dc; _uetvid=26806d80af3911eeb220518954a7de61; _derived_epik=dj0yJnU9NER1cmVSY0ZMLU1LcElfUnVmT2lZY3pZcEhWVmszWTAmbj1MMXJpOGw0akdobmhLeWxjWC1jQkdnJm09NCZ0PUFBQUFBR1dlQ0drJnJtPTQmcnQ9QUFBQUFHV2VDR2smc3A9Mg; _ga_46SXWPZP8L=GS1.3.1704855657.4.0.1704855657.0.0.0; _ga_1H4VG5F5JF=GS1.1.1704855642.4.1.1704855665.0.0.0"
    ]
}

response = requests.post(url, json=payload, headers=headers)

# Check if response is successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract information
    extracted_data = {
        'title': soup.title.string if soup.title else "No title found",
        'meta_description': soup.find('meta', attrs={'name': 'description'}).get('content') if soup.find('meta', attrs={'name': 'description'}) else "No description found",
        'links': [{'href': link['href'], 'text': link.get_text(strip=True)} for link in soup.find_all('a', href=True)]
    }

    # Save the extracted data to a JSON file
    file_path = 'C:\\Users\\luizm\\casaconforto\\python_base\\extracted_data.json'
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(extracted_data, f, ensure_ascii=False, indent=4)

    print(f"Extracted data saved to {file_path}")

else:
    print(f"Failed to scrape the website. Status code: {response.status_code}")