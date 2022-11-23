# Server side rendering

# As 3 etapas aqui serão:
 # - Carregar os dados (Dados de API, arquivos, banco de dados etc)
 # - Processar (Definir templates de visualização)
 # - Renderizar

dados = [
    {"nome": "Alexandre", "cidade": "Viana"},
    {"nome": "Guido", "cidade": "Amsterdan"}
]
# Criamos o template (visualização) definidos seus placeholders
template = """\ 
<html>
<body>
    <ul>
        <li> Nome: {dados[nome]}</li>
        <li> Cidade: {dados[cidade]}</li>
    </ul>
</body>
</html>
"""
for item in dados:
    print(template.format(dados=item))