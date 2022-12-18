import cgi
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

def add_new_post(post):
    cursor = conn.cursor()
    cursor.execute(
        """\
        INSERT INTO post (title, content, author)
        VALUES (:title, :content, :author)
        """,
        post, # Na sintexe acima, basta passar o dict que o sqlite lê o conteúdo e salva
    )
    conn.commit()

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
        status = '200 OK'
    elif path == "/new" and method =="GET":
        body = render_template("form.template.html")
        status = "200 OK"
    elif path == "/new" and method =="POST":
        form = cgi.FieldStorage(
            fp = environ["wsgi.input"], # Intercepta os inputs de formulários
            environ = environ,
            keep_blank_values=1 # O wsgi não envia informações de campos em branco. Isso pode quebrar o código. Por isso setamos o valor dessa variável
        )
        post = {item.name: item.value for item in form.list} # Conteúdo do POST. Pegamos usando o obheto form do cgi
        add_new_post(post) # Insert do post no banco de dados
        body = b"New post created with success!" # Body após salvar post
        status = "201 Created"

    # Criar o response
    headers = [("Content-type", "text/html")]
    start_response(status, headers)
    return [body]