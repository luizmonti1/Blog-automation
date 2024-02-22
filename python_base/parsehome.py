import bs4 # BeautifulSoup
from bs4 import BeautifulSoup



# Function to update specific elements of HTML content
def update_homepage_html(html_content, new_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Example: Update the main heading (h1)
    h1_tag = soup.find('h1')
    if h1_tag and isinstance(h1_tag, bs4.element.Tag):
        h1_tag.string = new_content['main_heading']

    # Example: Update paragraph content
    p_tags = soup.find_all('p')
    for i, p_tag in enumerate(p_tags):
        if i < len(new_content['paragraphs']):
            if isinstance(p_tag.string, bs4.element.Tag):
                p_tag.string = new_content['paragraphs'][i]

    return str(soup)

# Read the original HTML file
with open('C:\\Users\\luizm\\CasaConforto\\python_base\\homepage.html', 'r', encoding='utf-8') as file:
    original_html_content = file.read()

# New content to be added (this is just an example, modify as needed)
new_content = {
    'main_heading': 'Welcome to Casa Conforto',
    'paragraphs': [
        'Discover the art of home decoration and organization.',
        'Tips and tricks for a comfortable and stylish living space.'
    ]
}

# Update the HTML content
updated_html_content = update_homepage_html(original_html_content, new_content)

# Write the updated content to a new file
with open('path_to_updated_html_file.html', 'w', encoding='utf-8') as file:
    file.write(updated_html_content)
