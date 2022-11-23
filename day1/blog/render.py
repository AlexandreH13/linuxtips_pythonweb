# 1 - Obtém dados do db
# 2 - Cria pasta de destino do blog
# 3 - Cria uma função que gera url (usando slug, que é a utl mais enxuta)
# 4 - Renderizar a página index
# 5 - Renderizar as páginas do blog

from pathlib import Path
from database import conn

cursor = conn.cursor()
fields = ("id", "title", "content", "author")
results = cursor.execute("SELECT * FROM post;") # Objeto iterável com tuplas representando nossos posts
posts = [dict(zip(fields, post)) for post in results]

site_dir = Path("site") # Pasta onde teremos os resultados das renderizações
site_dir.mkdir(exist_ok=True) # Cria pasta se ela não existir

def get_post_url(post):
    """Função que gera a url da nossa
    renderização.

    Args:
        post (list): List com os posts consultados no nosso banco de dados
    """
    slug = post["title"].lower().replace(" ", "-") # Geramos a url com o título do nosso post
    return f"{slug}.html"

# Vamos pegar nossos posts para "alimentar" a página index
# Na index vamos passar apenas os títulos
index_template = Path("list_template.html").read_text() # Lendo o html como texto para passar as informações lidas do banco e formatar o texto
index_page = site_dir / Path("index.html")
post_list = [
    f"<li> <a href='{get_post_url(post)}'>{post['title']} </a> </li>" # Vamos usar a função criada acima para passar a url criada para o post
    for post in posts
]
index_page.write_text( # Texo que vamos escrever na página
    index_template.format(post_list="\n".join(post_list)) # Estamos o lendo o html como um texto, por isso podemos usar o format e passar o post_list
)

# Etapa 5
for post in posts:
    post_templat = Path("post_template.html").read_text()
    post_page = site_dir / Path(get_post_url(post))
    post_page.write_text(post_templat.format(post=post))

print("Site geenerated!")

conn.close()