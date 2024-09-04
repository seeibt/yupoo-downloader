import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configura o Selenium para usar o ChromeDriver
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Abre a página do Yupoo
url = 'https://hongxin1.x.yupoo.com/categories/3512611?page=5'
driver.get(url)

# Espera explícita para garantir que a página inicial carregue completamente
wait = WebDriverWait(driver, 10)

def process_album(album_link):
    album_name = None  # Inicializa album_name para uso no bloco except
    try:
        # Coleta o nome do álbum e a URL, substitui barras invertidas por pontos
        album_name = album_link.get_attribute('title').replace("\\", ".").replace("/", ".")
        album_url = album_link.get_attribute('href')
        
        # Cria uma pasta com o nome do álbum
        os.makedirs('Sneakers/SB Dunk/' + album_name, exist_ok=True)
        
        # Navega para a página do álbum
        driver.get(album_url)
        
        # Espera explícita para garantir que a página do álbum carregue completamente
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.image__imagewrap img')))
        
        # Rola para baixo para garantir que todas as imagens sejam carregadas
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Encontra todas as imagens dentro do álbum
        image_wrappers = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.image__imagewrap img')))
        
        for index, img in enumerate(image_wrappers):
            try:
                # Obtém a URL da imagem
                img_url = img.get_attribute('src')
                img_url = 'https:' + img_url if img_url.startswith('//') else img_url
                
                # Substitui 'small' por 'medium' na URL para obter a imagem em alta qualidade
                img_url = img_url.replace('small', 'medium')
                
                # Print da URL da imagem para verificação
                print(f'URL da imagem {index+1} do álbum "{album_name}": {img_url}')
                
                img_name = f'Sneakers/SB Dunk/{album_name}/image_{index+1}.jpg'
                
                # Faz o download da imagem e salva no diretório do álbum
                response = requests.get(img_url, headers={'Referer': album_url})
                if response.status_code == 200:
                    with open(img_name, 'wb') as f:
                        f.write(response.content)
                    print(f'Imagem {index+1} do álbum "{album_name}" baixada com sucesso.')
                else:
                    print(f'Erro ao baixar a imagem {index+1} do álbum "{album_name}". Status Code: {response.status_code}')
            except Exception as img_error:
                print(f'Erro ao processar a imagem {index+1} do álbum "{album_name}": {img_error}')
        
        # Volta para a página inicial e aguarda a atualização dos álbuns
        driver.get(url)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.album__main')))
        
    except Exception as e:
        print(f'Erro ao processar o álbum "{album_name}": {e}')

# Encontrar todos os links dos álbuns
def get_album_links():
    try:
        album_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.album__main')))
        return album_links
    except Exception as e:
        print(f'Erro ao encontrar links dos álbuns: {e}')
        return []

# Processar álbuns
processed_albums = set()
try:
    while True:
        album_links = get_album_links()
        if not album_links:
            break
        for album_link in album_links:
            try:
                album_href = album_link.get_attribute('href')
                if album_href not in processed_albums:
                    process_album(album_link)
                    processed_albums.add(album_href)
            except Exception as e:
                print(f'Erro ao processar o álbum: {e}')
        # Espera um pouco antes de tentar recarregar a lista de álbuns
        driver.refresh()
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a.album__main')))
finally:
    # Fecha o navegador
    driver.quit()

print('Todas as imagens foram baixadas com sucesso.')
