from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from sql import engine, Veiculos, VistoriaImagens
from sqlalchemy.orm import sessionmaker, session
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from sqlalchemy.exc import IntegrityError
from urllib.parse import urljoin
from dotenv import load_dotenv
from selenium import webdriver
from datetime import datetime
from bs4 import BeautifulSoup
import pyautogui
import paramiko
import requests
import shutil
import time
import os


# Obter as credenciais a partir das variáveis de ambiente
username = os.getenv('APP_USERNAME')
password = os.getenv('APP_PASSWORD')

# Obter as credenciais do arquivo .env
host_ssh = os.getenv('HOST_SSH')
port_ssh = int(os.getenv('PORT_SSH'))  # Converte para inteiro
username_ssh = os.getenv('USERNAME_SSH')
password_ssh = os.getenv('PASSWORD_SSH')
# remote_folder = "/var/www/imagens_vistorias/"

# Configura o caminho para o ChromeDriver
chrome_driver_path = r'C:\Users\rafae\Downloads\chromedriver-win64\chromedriver.exe' 

# Verifica se o arquivo chromedriver.exe existe
if not os.path.isfile(chrome_driver_path):
    raise FileNotFoundError(f"O arquivo chromedriver.exe não foi encontrado no caminho especificado: {chrome_driver_path}")

# Configura o navegador
options = Options()
options.add_argument("--start-maximized")  # Maximiza a janela do navegador
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

# Abre a página de login
driver.get('https://www.hitex.com.br/')

# Espera explícita para garantir que o elemento esteja presente
time.sleep(3)  # Aguarde o carregamento da página
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
driver.get('https://www.hitex.com.br/plataforma/index.php?p=gestor-administrativo&g=0')  

time.sleep(10)

# Espera até que o modal esteja visível
modal_selector = 'modal-body'  # Substitua pelo seletor que corresponde ao modal
driver.implicitly_wait(10)  # Espera implícita para o modal

# Localiza todos os botões "VER" na página
botoes_ver = driver.find_elements(By.CSS_SELECTOR, 'a.info_sinistro')
print(f"Total de botões encontrados: {len(botoes_ver)}")

for index, botao in enumerate(botoes_ver):
    try:
        print(f"Acessando botão {index + 1} de {len(botoes_ver)}")
                      
        # Scroll até o botão para garantir que ele esteja visível
        ActionChains(driver).move_to_element(botao).perform()
        
        # Clica no botão para abrir o modal
        # botao.click()
        time.sleep(25)  # Aguarde o modal carregar
        
        # Extrai o HTML da página
        html = driver.page_source
        
        # Analisa o HTML com BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # --- DADOS DO SINISTRO ---
        sinistro_tab = soup.find('div', {'class': 'ltab', 'id': 'ldados'})
        if sinistro_tab:
            print("=== DADOS DO SINISTRO ===")
            campos = [
                "Veículos:",
                "Integrante:",
                "Data de Ocorrência:",
                "Status:",
                "Estado:",
                "Cidade:",
                "Tipo:",
                "Código:",
                "Responsabilidade:"
            ]
            for campo in campos:
                b_tag = sinistro_tab.find('b', string=campo)
                if b_tag:
                    # Para "Status:", pode estar dentro de uma div.label
                    if campo == "Status:":
                        label = b_tag.find_next('div', class_='label')
                        valor = label.get_text(strip=True) if label else ""
                    # Para "Código:", pode estar dentro de uma span.label
                    elif campo == "Código:":
                        label = b_tag.find_next('span', class_='label')
                        valor = label.get_text(strip=True) if label else ""
                    elif campo == "Veículos:":
                        # Captura todas as placas separadas por '#'
                        veiculos = []
                        sibling = b_tag.next_sibling
                        while sibling:
                            if sibling.name == 'span' and sibling.find('b'):
                                veiculos.append(sibling.find('b').get_text(strip=True))
                            elif sibling.string and sibling.string.strip() != "#":  # Ignora o caractere '#'
                                veiculos.append(sibling.string.strip())
                            sibling = sibling.next_sibling
                        print(f"{campo} {', '.join(veiculos)}")  # Exibe todas as placas
                        continue
                    else:
                        # O valor geralmente está logo após o <b>
                        valor = b_tag.next_sibling
                        if valor:
                            valor = valor.strip()
                        else:
                            valor = ""
                    print(f"{campo} {valor}")

            # Descrição Privada e Pública
            wells = sinistro_tab.find_all('div', class_='well')
            if len(wells) > 0:
                print("Descrição Privada:", wells[0].get_text(strip=True))
            if len(wells) > 1:
                print("Descrição Pública:", wells[1].get_text(strip=True))
        else:
            print("Dados do sinistro não encontrados.")
    
        # --- DADOS DO COMUNICANTE ---
        comunicante_tab = soup.find('div', {'class': 'ltab', 'id': 'lcomunicante'})
        if comunicante_tab:
            print("\n=== DADOS DO COMUNICANTE ===")
            campos = [
                "Nome:",
                "CPF:",
                "Estado:",
                "Cidade:",
                "Contato 1:",
                "Contato 2:",
                "Status:",
                "Primeiro Contato:"
            ]
            for campo in campos:
                b_tag = comunicante_tab.find('b', string=campo)
                if b_tag:
                    # Para "Status:", pode estar dentro de uma div.label
                    if campo == "Status:":
                        label = b_tag.find_next('div', class_='label')
                        valor = label.get_text(strip=True) if label else ""
                    else:
                        valor = b_tag.next_sibling
                        if valor:
                            valor = valor.strip()
                        else:
                            valor = ""
                    print(f"{campo} {valor}")
            # Narrativa
            narrativa = comunicante_tab.find('div', class_='well')
            if narrativa:
                print("Narrativa:", narrativa.get_text(strip=True))
        else:
            print("Dados do comunicante não encontrados.")
            
    except Exception as e:
        print(f"Erro ao processar sinistro {index}: {e}")
