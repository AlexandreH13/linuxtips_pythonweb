# Exigências WSGI
# 1 - callable
# 2 - Environ
# 3 - Função de callback com retorno iterável

from wsgiref.simple_server import make_server

def application(environ, start_response):
    # Faz o que quiser com o request

    # mostrar o response
    status = "200 Ok"
    headers = [("Content-type", "text/html")]
    body = b"<strong>Hello World</strong>" # Texto que vai no response. Tem que ser no formato bytes
    start_response(status, headers)
    return [body] # Colocamos em uma lista para retornar um iterável

#if __name__ == "__main__":
    
#    server = make_server("0.0.0.0", 8000, application)
#    server.serve_forever() # Executa