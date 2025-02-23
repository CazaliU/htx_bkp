from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from selenium import webdriver
from bs4 import BeautifulSoup
import pyautogui
import time
import os

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Obter as credenciais a partir das variáveis de ambiente
username = os.getenv('APP_USERNAME')
password = os.getenv('APP_PASSWORD')

x1, y1 = 33, 659


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

pyautogui.click(x1, y1)

time.sleep(3)

try:
    # Espera até que o modal esteja visível
    modal_selector = 'modal-body'  # Substitua pelo seletor que corresponde ao modal
    driver.implicitly_wait(10)  # Espera implícita para o modal

    # Extrai o HTML da página
    html = driver.page_source

    # Analisa o HTML com BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Captura os dados de status, inclusão e vigência do contrato
    status = soup.find('div', class_='label label-success').text.strip()
    inclusao = soup.find('div', class_='sub_status').find_all('span')[0].next_sibling.strip()
    vigencia = soup.find('div', class_='sub_status').find_all('span')[1].next_sibling.strip()

    print(f"Status: {status}")
    print(f"Inclusão: {inclusao}")
    print(f"Vigência do Contrato: {vigencia}")

    # Captura a Razão Social, CNPJ, Nome, Nacionalidade, Estado Civil, Profissão, RG, Orgão Exp, CPF e Nascimento
    elementos = soup.find_all('div', class_='six columns fv')
    razao_social = None
    cnpj = None
    nome = None
    nacionalidade = None
    estado_civil = None
    profissao = None
    rg = None
    orgao_exp = None
    cpf = None
    nascimento = None
    logradouro = None
    numero = None
    bairro = None
    cep = None
    complemento = None
    referencia = None
    estado = None
    cidade = None
    celular_preferencial = None
    celular_complementar = None
    telefone = None
    email = None

    for elemento in elementos:
        texto = elemento.text.strip()
        if texto.startswith("Razão Social:"):
            razao_social = texto.replace("Razão Social:", "").strip()
        elif texto.startswith("CNPJ:"):
            cnpj = texto.replace("CNPJ:", "").strip()
        elif texto.startswith("Nome:"):
            nome = texto.replace("Nome:", "").strip()
        elif texto.startswith("Nacionalidade:"):
            nacionalidade = texto.replace("Nacionalidade:", "").strip()
        elif texto.startswith("Estado Civil:"):
            estado_civil = texto.replace("Estado Civil:", "").strip()
        elif texto.startswith("Profissão:"):
            profissao = texto.replace("Profissão:", "").strip()
        elif texto.startswith("RG:"):
            rg = texto.replace("RG:", "").strip()
        elif texto.startswith("Orgão Exp:"):
            orgao_exp = texto.replace("Orgão Exp:", "").strip()
        elif texto.startswith("CPF:"):
            cpf = texto.replace("CPF:", "").strip()
        elif texto.startswith("Nascimento:"):
            nascimento = texto.replace("Nascimento:", "").strip()
        elif texto.startswith("Logradouro:"):
            logradouro = texto.replace("Logradouro:", "").strip()
        elif texto.startswith("Número:"):
            numero = texto.replace("Número:", "").strip()
        elif texto.startswith("Bairro:"):
            bairro = texto.replace("Bairro:", "").strip()
        elif texto.startswith("CEP:"):
            cep = texto.replace("CEP:", "").strip()
        elif texto.startswith("Complemento:"):
            complemento = texto.replace("Complemento:", "").strip()
        elif texto.startswith("Referência:"):
            referencia = texto.replace("Referência:", "").strip()
        elif texto.startswith("Estado:"):
            estado = texto.replace("Estado:", "").strip()
        elif texto.startswith("Cidade:"):
            cidade = texto.replace("Cidade:", "").strip()
        elif texto.startswith("Celular Preferencial:"):
            celular_preferencial = texto.replace("Celular Preferencial:", "").strip()
        elif texto.startswith("Celular Complementar:"):
            celular_complementar = texto.replace("Celular Complementar:", "").strip()
        elif texto.startswith("Telefone:"):
            telefone = texto.replace("Telefone:", "").strip()
        elif texto.startswith("E-mail:"):
            email = texto.replace("E-mail:", "").strip()
        elif texto.startswith("Vigência do Contrato:"):
            vigencia_contrato = texto.replace("Vigência do Contrato:", "").strip()
        elif texto.startswith("Método de Cobrança:"):
            metodo_cobranca = texto.replace("Método de Cobrança:", "").strip()
        elif texto.startswith("Índice de Participação Padrão:"):
            indice_participacao = texto.replace("Índice de Participação Padrão:", "").strip()
        elif texto.startswith("Integração TrackBrasil:"):
            integracao_trackbrasil = texto.replace("Integração TrackBrasil:", "").strip()

    print(f"Razão Social: {razao_social}")
    print(f"CNPJ: {cnpj}")
    print(f"Nome: {nome}")
    print(f"Nacionalidade: {nacionalidade}")
    print(f"Estado Civil: {estado_civil}")
    print(f"Profissão: {profissao}")
    print(f"RG: {rg}")
    print(f"Orgão Exp: {orgao_exp}")
    print(f"CPF: {cpf}")
    print(f"Nascimento: {nascimento}")
    print(f"Logradouro: {logradouro}")
    print(f"Número: {numero}")
    print(f"Bairro: {bairro}")
    print(f"CEP: {cep}")
    print(f"Complemento: {complemento}")
    print(f"Referência: {referencia}")
    print(f"Estado: {estado}")
    print(f"Cidade: {cidade}")
    print(f"Celular Preferencial: {celular_preferencial}")
    print(f"Celular Complementar: {celular_complementar}")
    print(f"Telefone: {telefone}")
    print(f"E-mail: {email}")
    print(f"Vigência do Contrato: {vigencia_contrato}")
    print(f"Método de Cobrança: {metodo_cobranca}")
    print(f"Índice de Participação Padrão: {indice_participacao}")
    print(f"Integração TrackBrasil: {integracao_trackbrasil}")

except Exception as e:
    print(f"Erro ao localizar os dados: {e}")

finally:
    # Fecha o navegador
    driver.quit()