# Na aula anterior criamos a parte client(http_client.py) que faz as requisições.
# Agora vamos criar o server

import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Criamos intancia do socker (Conexão HTTP)
server.bind(("localhost", 9000)) # Realiza o bind (acopla) do socket com HTTP e a porta
server.listen() # Faz o socket passar a ouvir conexões

# Loop de eventos para permitir com que o server fique escutando na porta e quantos clientes necessários
try:

    # Qualquer cliente que enviar uma requisição, vamos aceitar a conexão
    while True:
        client, address = server.accept() # Pegamos uma instância do cliente e seu endereço

        # Request
        data = client.recv(5000).decode() # Pegamos os dados do request do cliente com a instancia client. Recebemos um tamanho máximo de 5000 bytes
        print(f"{data=}")

        # Response
        client.sendall(
            # Criamos o objeto response usando a estrutura padrão de resposta do HTTP
            "HTTP/1.0 200 OK\r\n\r\n<html><body>Hello</body></html>\r\n\r\n".encode()
        )
        client.shutdown(socket.SHUT_WR)

except Exception:
    server.close()

server.close() # Fechamos a conexão para liberar a porta