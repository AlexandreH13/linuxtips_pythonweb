# Podemo abstrair todo aquele código do script
# http_client.py usando algumas libs já prontas

from urllib.request import urlopen
import requests
import httpx

# usando urllib
result = urlopen("http://example.com/index.html")
#print(result)

# usando requests
# essa lib implementa os métodos (get, post etc)
#result = requests.get("http://example.com/index.html")
#print(result.header())

# Usando httpx
result = httpx.get("http://example.com/index.html")
print(result.status_code)
print(result.headers)
print(result.content)