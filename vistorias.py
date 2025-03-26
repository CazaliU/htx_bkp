from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from sqlalchemy.orm import sessionmaker, session
from selenium.webdriver.common.by import By
from sqlalchemy.exc import IntegrityError
from sql import engine, Veiculos
from dotenv import load_dotenv
from selenium import webdriver
from bs4 import BeautifulSoup
import pyautogui
import time
import os


# Obter as credenciais a partir das variáveis de ambiente
username = os.getenv('APP_USERNAME')
password = os.getenv('APP_PASSWORD')

# Configura o caminho para o ChromeDriver
chrome_driver_path = r'C:\Users\rafae\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'  # Caminho atualizado

# Verifica se o arquivo chromedriver.exe existe
if not os.path.isfile(chrome_driver_path):
    raise FileNotFoundError(f"O arquivo chromedriver.exe não foi encontrado no caminho especificado: {chrome_driver_path}")

# Configura o navegador
options = Options()
options.add_argument("--start-maximized")  # Maximiza a janela do navegador
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

# Abre a página de login
driver.get('https://www.hitex.com.br/')  # Substitua pela URL real do login

# Espera explícita para garantir que o elemento esteja presente
wait = WebDriverWait(driver, 10)
username_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Usuário"]')
password_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Senha"]')
submit_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')

username_input.send_keys(username)  # Substitua pelo seu nome de usuário
password_input.send_keys(password)  # Substitua pela sua senha
submit_button.click()

# Aguarde a página carregar
time.sleep(3)  # Pode ser necessário ajustar o tempo

# Navega para a página onde está o status
driver.get('https://www.hitex.com.br/plataforma/index.php?p=gestor-administrativo&g=0')  # Substitua pela URL real da página

# Aguarde a página carregar
# time.sleep(180)  

time.sleep(10)

# Espera até que o modal esteja visível
modal_selector = 'modal-body'  # Substitua pelo seletor que corresponde ao modal
driver.implicitly_wait(10)  # Espera implícita para o modal

# Extrai o HTML da página
html = driver.page_source

# Analisa o HTML com BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Lista para armazenar as informações de todas as vistorias
vistorias = []

# Encontra todas as divs com a classe 'subport default listar_anexos'
vistoria_divs = soup.find_all('div', class_='subport default listar_anexos')

for vistoria in vistoria_divs:
    # Captura o conteúdo da div 'caption'
    caption_div = vistoria.find('div', class_='caption')
    
    # Inicializa as variáveis
    numero, data_hora, nome, telefone = None, None, None, None

    if caption_div:
        caption_text = caption_div.text.strip()
        partes = caption_text.split('#')
        if len(partes) >= 5:
            numero = partes[1].strip()
            data_hora = partes[2].strip()
            nome = partes[3].strip()
            telefone = partes[4].strip()

    # Captura o status
    status_span = vistoria.find('span', class_='label')
    status = status_span.text.strip() if status_span else "Status não encontrado"

    # Captura os atributos 'alt' e os links das imagens
    imagens = []
    imagens_div = vistoria.find_all('div', class_='dz-image')
    
    for imagem_div in imagens_div:
        img_tag = imagem_div.find('img')
        if img_tag:
            alt_text = img_tag.get('alt', 'Sem descrição')
            src_link = img_tag.get('src', '')
            imagens.append({'alt': alt_text, 'src': src_link})

    # Adiciona as informações capturadas à lista
    vistorias.append({
        'numero': numero,
        'data_hora': data_hora,
        'nome': nome,
        'telefone': telefone,
        'status': status,
        'imagens': imagens
    })

# Exibe as informações capturadas
for vistoria in vistorias:
    print(f"Número: {vistoria['numero']}")
    print(f"Data e Hora: {vistoria['data_hora']}")
    print(f"Nome: {vistoria['nome']}")
    print(f"Telefone: {vistoria['telefone']}")
    print(f"Status: {vistoria['status']}")
    print("Imagens:")
    for img in vistoria['imagens']:
        print(f"  - {img['alt']} ({img['src']})")
    print("-" * 50)