import os
import re

# Caminho para a pasta onde estão as subpastas que deseja renomear
caminho_pasta = "caminho/para/suas/pastas"

# Regex para identificar caracteres não latinos (exclui letras e números comuns, além de espaços)
pattern = re.compile(r'[^\x00-\x7F]')

# Percorre todas as pastas no diretório especificado
for nome_pasta in os.listdir(caminho_pasta):
    novo_nome = pattern.sub('', nome_pasta)  # Remove os caracteres não latinos
    novo_nome = novo_nome.replace("  ", " ")  # Remove espaços duplos
    novo_nome = novo_nome.strip()  # Remove espaços extras nas extremidades
    
    if nome_pasta != novo_nome:
        os.rename(os.path.join(caminho_pasta, nome_pasta), os.path.join(caminho_pasta, novo_nome))
        print(f'Renomeado: "{nome_pasta}" para "{novo_nome}"')
