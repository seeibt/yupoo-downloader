import os
import re

# Caminho para a pasta onde estão as subpastas que deseja renomear
caminho_pasta = "Sneakers/SB Dunk/"

# Regex para identificar caracteres não latinos (exclui letras e números comuns, além de espaços)
pattern = re.compile(r'[^\x00-\x7F]')

# Função para gerar um novo nome de pasta caso o original já exista
def gerar_nome_unico(caminho_pasta, novo_nome):
    contador = 2
    nome_unico = novo_nome
    while os.path.exists(os.path.join(caminho_pasta, nome_unico)):
        nome_unico = f"{novo_nome} ({contador})"
        contador += 1
    return nome_unico

# Percorre todas as pastas no diretório especificado
for nome_pasta in os.listdir(caminho_pasta):
    novo_nome = pattern.sub('', nome_pasta)  # Remove os caracteres não latinos
    novo_nome = novo_nome.replace("  ", " ")  # Remove espaços duplos
    novo_nome = novo_nome.strip()  # Remove espaços extras nas extremidades
    
    if nome_pasta != novo_nome:
        # Gera um nome único se o novo nome já existir
        novo_nome_unico = gerar_nome_unico(caminho_pasta, novo_nome)
        os.rename(os.path.join(caminho_pasta, nome_pasta), os.path.join(caminho_pasta, novo_nome_unico))
        print(f'Renomeado: "{nome_pasta}" para "{novo_nome_unico}"')
