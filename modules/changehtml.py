from bs4 import BeautifulSoup
import os
import polib  # For .po file parsing and compiling

# Directories where your HTML and PHP files are stored
directories = [
    'C:\\Users\\luizm\\CasaConforto\\templates',
    'C:\\Users\\luizm\\CasaConforto\\languages',
    'C:\\Users\\luizm\\CasaConforto\\patterns',
    'C:\\Users\\luizm\\CasaConforto\\parts'
]

# Dictionary with your new SEO data
seo_data = {
    'meta_description': 'Descubra dicas de decoração e organização para tornar sua casa um lar confortável.',
    'meta_keywords': 'casa, decoração, organização, bem-estar, conforto',
    # Add more as needed
}

# Function to update SEO related content
def update_seo_content(file_path, seo_data):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Use BeautifulSoup for HTML files
    if file_path.endswith('.html'):
        soup = BeautifulSoup(content, 'html.parser')
        # Update meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            meta_desc['content'] = str(seo_data['meta_description'])
        
        # Update meta keywords
        meta_keys = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keys:
            meta_keys['content'] = str(seo_data['meta_keywords'])
        
        # Save changes to the HTML file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))
    else:
        # For PHP or other file types, you may want to perform regex replacements
        # This is just a placeholder and needs to be customized
        pass

# Walk through the directories and update each file
for directory in directories:
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html') or file.endswith('.php'):
                update_seo_content(os.path.join(subdir, file), seo_data)

# Load and compile the .po file to a .mo file
po_file_path = 'C:\\Users\\luizm\\CasaConforto\\languages\\pt_BR.po'
mo_file_path = 'C:\\Users\\luizm\\CasaConforto\\languages\\pt_BR.mo'

# Load the .po file
po = polib.pofile(po_file_path)

# Update translations
translations = {
    "Creatio 2": "Creatio 2 Conforto",
    "https://wordpress.com/theme/creatio-2": "https://wordpress.com/theme/creatio-2-conforto",
    # Add your translations here
    # Example: "msgid": "msgstr"
}

for entry in po:
    if entry.msgid in translations:
        entry.msgstr = translations[entry.msgid]

# Save changes to the .po file and compile to .mo file
po.save()
po.save_as_mofile(mo_file_path)

print('SEO content update completed.')
