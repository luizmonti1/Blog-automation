from bs4 import BeautifulSoup
import os

def remove_unwanted_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    for link in soup.find_all('a', href=True):
        if 'external_site.com' in link['href']:  # Replace with specific criteria
            link.decompose()
    return str(soup)

def add_alt_to_images(html_content, default_alt="Image description"):
    soup = BeautifulSoup(html_content, 'html.parser')
    for img in soup.find_all('img', alt=False):
        img['alt'] = default_alt
    return str(soup)

def process_html_files(directory):
    for subdir, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(subdir, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                content = remove_unwanted_links(content)
                content = add_alt_to_images(content)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

def add_basic_responsive_css(css_file_path):
    responsive_css = "@media screen and (max-width: 600px) {\n    .sidebar {\n        display: none;\n    }\n}\n"
    with open(css_file_path, 'a', encoding='utf-8') as file:
        file.write(responsive_css)

# Directory containing HTML files
html_directory = ''  # Update with your directory path

# Process all HTML files in the directory
process_html_files(html_directory)

# Add responsive CSS to the CSS file
css_file_path = ''
add_basic_responsive_css(css_file_path)
