from database import conn
from pathlib import Path


def get_posts_from_database(post_id=None):
    """
    Pega os post por id
    """
    cursor = conn.cursor()
    fields = ("id", "title", "content", "author")

    if post_id:
        results = cursor.execute("SELECT * FROM post WHERE id = ?;", post_id)
    else:
        results = cursor.execute("SELECT * FROM post;")

    return [dict(zip(fields, post)) for post in results]

def render_template(template_name, **context):
    template = Path(template_name).read_text()
    return template.format(**context).encode("utf-8")

def get_post_list(posts):
    post_list = [
        f"""<li><a href="/{post['id']}">{post['title']}</a></li>"""
        for post in posts
    ]
    return "\n".join(post_list)

def application(environ, start_response):
    body = b"Content Not Found"
    status = "404 Not Found"
    # Pricessar o request
    """
    Pegamos o path passado pela url pelo usuário.
    Obtemos esse path por uma variável de ambiente
    chamada PATH INFO. Pegamos também qual foi o 
    request method
    """
    path = environ["PATH_INFO"]
    method = environ["REQUEST_METHOD"]

    # Fazendo o roteamento de rotas
    if path == "/" and method == "GET": # Quer acessar a index
        # Mudamos o body e status padrão
        posts = get_posts_from_database()
        print(posts)
        body = render_template(
            "list.template.html", post_list=get_post_list(posts)
        )
        status = "200 Ok"

    elif path.split("/")[-1].isdigit() and method == "GET": # Quer acessar algum post. Pegando o id do post passado pela url
        post_id = path.split("/")[-1]
        body = render_template(
            "post.template.html",
            post=get_posts_from_database(post_id=post_id)[0]
        )

    # Criar o response
    headers = [("Content-type", "text/html")]
    start_response(status, headers)
    return [body]