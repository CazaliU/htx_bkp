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

load_dotenv()

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
time.sleep(5)  # Pode ser necessário ajustar o tempo

# Navega para a página onde está o status
driver.get('https://www.hitex.com.br/plataforma/index.php?p=gestor-administrativo&g=0')  # Substitua pela URL real da página

# Aguarde a página carregar
time.sleep(10)  

try:
    # Espera até que o modal esteja visível
    modal_selector = 'modal-body'  # Substitua pelo seletor que corresponde ao modal
    driver.implicitly_wait(10)  # Espera implícita para o modal

    # Extrai o HTML da página
    html = driver.page_source

    # Analisa o HTML com BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    status = None
    inclusao = None
    exclusao = None
    valor_cota = None


    # Tenta encontrar o elemento com a classe 'label label-success'
    status_element = soup.find('div', class_='label label-success')

    # Se não encontrar, tenta encontrar o elemento com a classe 'label label-danger'
    if not status_element:
        status_element = soup.find('div', class_='label label-danger')

    # Define o valor de 'status' com base no elemento encontrado
    if status_element:
        status = status_element.text.strip()
    else:
        status = 'Status não encontrado'

    # Captura os dados de inclusão e exclusão do contrato
    sub_status_elements = soup.find('div', class_='sub_status').find_all('span')
    if len(sub_status_elements) >= 1:
        inclusao = sub_status_elements[0].next_sibling.strip()
        if len(sub_status_elements) > 1:
            exclusao = sub_status_elements[1].next_sibling.strip()
            
    # Encontrar todas as tags <span> com a classe 'label label-grey'
    valor_cota_element = soup.find_all('span', class_='label label-grey')

    # Pegando o texto da primeira ocorrência
    if valor_cota_element:
        valor_cota = valor_cota_element[0].get_text(strip=True)

    print(f"Status: {status}")
    print(f"Inclusão: {inclusao}")
    print(f"Exclusão: {exclusao}")
    print(f"Valor da Cota: {valor_cota}")
    
    # Encontrar todos os elementos com a classe 'twelve columns fv', 'six columns fv', 'four columns fv', 'four columns fv input-button'
    elementos = soup.find_all('div', class_=['twelve columns fv', 'six columns fv', 'four columns fv', 'four columns fv input-button', 'twelve columns well branco'])
    
    integrante = None
    tipo = None
    especie = None
    composicao = None
    cod_fipe = None
    valor_principal = None
    agregado = None
    indice_participacao = None

    
    for elemento in elementos:
        texto = elemento.text.strip()
        if texto.startswith("Integrante:"):
            integrante = texto.replace("Integrante:", "").strip()
        elif texto.startswith("Tipo:"):
            tipo = texto.replace("Tipo:", "").strip()
        elif texto.startswith("Espécie:"):
            especie = texto.replace("Espécie:", "").strip()
        elif texto.startswith("Composição:"):
            composicao = texto.replace("Composição:", "").strip()
        elif texto.startswith("Cod. Fipe:"):
            cod_fipe = texto.replace("Cod. Fipe:", "").strip()
        elif texto.startswith("Valor Principal:"):
            valor_principal = texto.replace("Valor Principal:", "").strip()
        elif texto.startswith("Agregado:"):
            agregado = texto.replace("Agregado:", "").strip()
        elif texto.startswith("Índice de Participação:"):
            indice_participacao = texto.replace("Índice de Participação:", "").strip()

    # Inicializa dicionário para armazenar os valores
    dados_veiculo = {
        "marca": [],
        "modelo": [],
        "placa": [],
        "ano fabricação": [],
        "ano modelo": [],
        "renavam": [],
        "chassi": [],
        "cor": [],
        "estado": [],
        "cidade": [],
        "documento": [],
    }


    label_tag = elemento.find('b')
    if label_tag:
        label = label_tag.get_text(strip=True).replace(":", "")
        valor = label_tag.next_sibling.strip() if label_tag.next_sibling else ""
        if label.lower() in dados_veiculo:
            dados_veiculo[label.lower()].append(valor)
            

except Exception as e:
    print(f"Erro ao localizar os dados: {e}")

finally:
    # Fecha o navegador
    driver.quit()