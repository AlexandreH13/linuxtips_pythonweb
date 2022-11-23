from pydoc import cli
import socket # Socket precisa ser aberto dos dois lados (cliente e servidor)

# Com um socket apenas estabelecemos que vamos
# comunicar com o server através de uma porta,
# independente de qual for o tipo de comunicação,
# via http ou não
# Para configurar a comunicação com IPV4 usamos o AF_INET.
# Usamos o tipo de STREAM para trabalharmos com objetos de tipo texto.
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Fazendo conexão com o servidor. Passamos o endereço.
# Passando também através de qual porta vamos comunicar.
client.connect(("localhost", 9000))

# A partir do momento que estamos conectados com o servidor,
# podemos executar comandos. Criamos um comando para pegar,
# um recurso usando o método GET: a página index.html.
# Precisamos também passar o encode para usar um formato
# mais "cru" de texto para que o servidor entenda.
# Esse texto abaixo que montamos nada mais é que o request.
cmd = """\
GET http://localhost/index.html HTTP/1.0
User-Agent: Alexandre-Client/1.0

""".encode()
client.send(cmd)

# Criamos um streaming onde vamos receber "chuncks" de
# 512 bytes cada. Depois verificamos se não existe mais
# alguma informação e printamos. É necessário decodificar.
while True:

    data = client.recv(512)
    if len(data) < 1:
        break
    print(data.decode(), end="")

client.close()