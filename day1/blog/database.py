# Usando sqlite built-in do python

# 1 - Conexão
from sqlite3 import connect
conn = connect("blog.db")
cursor = conn.cursor()

# 2 Tabelas e colunas do banco
conn.execute(
    """
    CREATE TABLE if not exists post (
        id integer PRIMARY KEY AUTOINCREMENT,
        title varchar UNIQUE NOT NULL,
        content varchar NOT NULL,
        author varchar NOT NULL
    );
    """
)

posts = [
    {
        "title": "Python, a linguagem mais popular",
        "content": """\
        A linguagem python foi eleita a mais popular!
        """,
        "author": "Satoshi",
    },
    {
        "title": "Como criar um blog usando python",
        "content": """\
        Use python para criar seu próprio blog.
        """,
        "author": "Guido",
    }
]

# 4 - Inserimos os posts caso o banco dee dados esteja vazio
count = cursor.execute('SELECT * FROM post;').fetchall()
if not count:
    cursor.executemany(
        """\
        INSERT INTO post (title, content, author)
        VALUES (:title, :content, :author)
        """,
        posts
    )
    conn.commit()
# 5 - Verificamos que foi realmente inserido
posts = cursor.execute("SELECT * FROM post;").fetchall()
assert len(posts) >= 2