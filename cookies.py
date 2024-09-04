from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configura o Selenium para usar o ChromeDriver
chrome_options = Options()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Abre a página e insere a senha manualmente
url = 'https://hongxin1.x.yupoo.com/albums'
driver.get(url)

# Adicione um tempo de espera manual para você inserir a senha e completar o login
input("Pressione Enter após inserir a senha...")

# Captura os cookies
cookies = driver.get_cookies()

# Salva os cookies em um arquivo
import json
with open('cookies.json', 'w') as f:
    json.dump(cookies, f)

print("Cookies capturados e salvos.")

# Fecha o navegador
driver.quit()
