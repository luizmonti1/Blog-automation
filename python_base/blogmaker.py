import openai
import json
from typing import Dict, List

# OpenAI API Key
api_key = 'YOUR_API_KEY'
openai.api_key = api_key

# Your blog Body
body = [
    # wp:group {"layout":{"type":"constrained"}}
    '<div class="wp-block-group"><!-- wp:group {"layout":{"type":"constrained"}} -->',
    '<div class="wp-block-group"><!-- wp:paragraph -->',
    '<p>Com o aumento do trabalho remoto, o home office tornou-se um espaço essencial em nossas casas. Não é apenas um local de trabalho; é um ambiente onde passamos grande parte do nosso dia. Por isso, é crucial criar um espaço que não apenas seja funcional, mas também confortável e inspirador.</p>',
    '<!-- /wp:paragraph --></div>',
    '<!-- /wp:group -->',
    '',
    '<!-- wp:freeform -->',
    '<div class="wp-block-group">',
    '<!-- /wp:freeform -->',
    '',
    '<!-- wp:heading -->',
    '<h2 class="wp-block-heading">1. A Importância de um Espaço de Trabalho Adequado:</h2>',
    '<!-- /wp:heading -->',
    '',
    '<!-- wp:paragraph -->',
    '<p>Discutimos como um ambiente de trabalho bem organizado e confortável pode aumentar a produtividade e reduzir o estresse. Destacamos a importância de separar o espaço de trabalho das outras áreas da casa para manter um equilíbrio saudável entre trabalho e vida pessoal.</p>',
    '<!-- /wp:paragraph -->',
    '<!-- wp:paragraph -->',
    '<p><strong>Produto em destaque:</strong> <a href="LINK-DO-PRODUTO">Escrivaninha Trevalla Kuadra Me150-E10 Industrial 150cm Preto Onix</a> - Ideal para criar uma estação de trabalho ampla e elegante em casa.</p>',
    '<!-- /wp:paragraph -->',
    '',
    '<!-- wp:heading -->',
    '<h2 class="wp-block-heading">2. Mobiliário Ergonômico:</h2>',
    '<!-- /wp:heading -->',
    '',
    '<!-- wp:paragraph -->',
    '<p>Exploramos a importância de uma boa cadeira, como a "Cadeira de escritório ergonômica", para prevenir dores nas costas e outros problemas relacionados à postura.</p>',
    '<!-- /wp:paragraph -->',
    '',
    '<!-- wp:heading -->',
    '<h2 class="wp-block-heading">3. Acessórios Essenciais para Home Office:</h2>',
    '<!-- /wp:heading -->',
    '',
    '<!-- wp:paragraph -->',
    '<p>Descrevemos como suportes para laptop, como o "Suporte para laptop ajustável de alumínio", podem ajudar a manter uma postura ergonômica. Sugerimos o uso de organizadores, como o "Suporte Uptable OCTOO", para manter o espaço de trabalho limpo e organizado.</p>',
    '<!-- /wp:paragraph -->',
    '',
    '<!-- wp:paragraph -->',
    '<p>4. Personalizando seu Espaço de Home Office:</p>',
    '<!-- /wp:paragraph -->',
    '',
    '<!-- wp:paragraph -->',
    '<p>Oferecemos ideias para personalizar o espaço de trabalho em casa, tornando-o um local agradável e inspirador. Sugerimos o uso de plantas, iluminação adequada e elementos decorativos.</p>',
    '<!-- /wp:paragraph -->',
    '',
    '<!-- wp:heading -->',
    '<h2 class="wp-block-heading">4. Personalizando seu Espaço de Home Office:</h2>',
    '<!-- /wp:heading -->',
    '',
    '<!-- wp:paragraph -->',
    '<p>Enfatizamos como as medidas corretas são cruciais para a saúde e o bem-estar. Discutimos a altura ideal da mesa e do assento, e como organizar o espaço de trabalho de maneira eficiente.</p>',
    '<!-- /wp:paragraph -->',
    '',
    '<!-- wp:heading {"textAlign":"left","level":3} -->',
    '<h3 class="wp-block-heading has-text-align-left">Maximizando Espaço no Home Office:</h3>',
    '<!-- /wp:heading -->',
    '',
    '<!-- wp:paragraph -->',
    '<p>Apresentamos soluções para espaços amplos e limitados, oferecendo opções para todos os tamanhos e orçamentos. Desde móveis multifuncionais até dicas de organização vertical, abordamos maneiras de otimizar o espaço em qualquer situação.</p>',
    '<!-- /wp:paragraph -->',
    '',
    '<!-- wp:columns -->',
    '<div class="wp-block-columns"><!-- wp:column {"width":"25%"} -->',
    '<div class="wp-block-column" style="flex-basis:25%"></div>',
    '<!-- /wp:column -->',
    '',
    '<!-- wp:column {"width":"50%"} -->',
    '<div class="wp-block-column" style="flex-basis:50%"></div>',
    '<!-- /wp:column -->',
    '',
    '<!-- wp:column {"width":"25%"} -->',
    '<div class="wp-block-column" style="flex-basis:25%"></div>',
    '<!-- /wp:column --></div>',
    '<!-- /wp:columns -->',
    '',
    '<!-- wp:paragraph -->',
    '<p>Encerramos destacando que um espaço de home office bem planejado e confortável é chave para um dia de trabalho produtivo e satisfatório. Lembre os leitores de que investir em seu espaço de trabalho é investir em seu bem-estar e sucesso profissional.</p>',
    '<!-- /wp:paragraph -->',
    '',
    '<!-- wp:columns -->',
    '<div class="wp-block-columns"><!-- wp:column {"width":"25%"} -->',
    '<div class="wp-block-column" style="flex-basis:25%"></div>',
    '<!-- /wp:column -->',
    '',
    '<!-- wp:column {"width":"50%"} -->',
    '<div class="wp-block-column" style="flex-basis:50%"></div>',
    '<!-- /wp:column -->',
    '',
    '<!-- wp:column {"width":"25%"} -->',
    '<div class="wp-block-column" style="flex-basis:25%"></div>',
    '<!-- /wp:column --></div>',
    '<!-- /wp:columns -->',
    '',
    '<!-- wp:paragraph -->',
    '<p>Convidamos os leitores a explorarem os produtos mencionados e a transformarem seus espaços de home office.</p>',
    '<!-- /wp:paragraph -->',
    '',
    '<!-- wp:group {"layout":{"type":"constrained"}} -->',
    '<div class="wp-block-group"><!-- wp:heading -->',
    '<h2 class="wp-block-heading">Produtos Adicionais para o Seu Home Office:</h2>',
    '<!-- /wp:heading -->',
    '',
    '<!-- wp:list -->',
    '<ul><!-- wp:list-item -->',
    '<li><a href="LINK-DO-PRODUTO">Cadeira Gamer Profissional TGC12 Preta ThunderX3</a> - Para os entusiastas de jogos que também precisam de uma cadeira confortável para trabalhar.</li>',
    '<!-- /wp:list-item -->',
    '',
    '<!-- wp:list-item -->',
    '<li><a href="LINK-DO-PRODUTO">Mesa Portátil Para Notebook</a> - Solução ideal para quem tem espaço limitado.</li>',
    '<!-- /wp:list-item -->',
    '',
    '<!-- wp:list-item -->',
    '<li><a href="LINK-DO-PRODUTO">Estante Para Livros Ditália</a> - Mantenha seus livros e documentos organizados e de fácil acesso.</li>',
    '<!-- /wp:list-item -->',
    '',
    '<!-- wp:list-item -->',
    '<li><a href="LINK-DO-PRODUTO">Kit 6 Caixas Organizadoras 56 Litros</a> - Perfeito para armazenar diversos itens e manter a ordem no seu espaço de trabalho.</li>',
    '<!-- /wp:list-item -->',
    '',
    '<!-- wp:list-item -->',
    '<li>    <br></li>',
    '<!-- /wp:list-item --></ul>',
    '<!-- /wp:list --></div>',
    '<!-- /wp:group --></div>',
    '<!-- /wp:group -->'
]

# Generating Blog Posts
def generate_blog_posts(body: List[str]) -> Dict[str, str]:
    client = openai.ChatCompletion(api_key=api_key)
    posts = {}
    for topic in body:
        response = client.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a creative assistant."},
                {"role": "user", "content": f"Improve this blog post: {topic}"}
            ]
        )
        response_data = response.choices[0].message.content.strip()
        posts[topic] = response_data
    return posts

# Saving Blog Posts to a JSON File
def save_posts_to_json(posts, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(posts, file, ensure_ascii=False, indent=4)

# Example Usage
blog_posts = generate_blog_posts(body)
json_file_path = 'C:\\Users\\luizm\\CasaConforto\\python_base\\blog_posts.json'  # Adjust this path as needed
save_posts_to_json(blog_posts, json_file_path)

print(f"Blog posts saved to {json_file_path}")
