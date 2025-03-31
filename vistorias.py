from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from sqlalchemy.orm import sessionmaker, session
from selenium.webdriver.common.by import By
from sqlalchemy.exc import IntegrityError
from sql import engine, Veiculos
from urllib.parse import urljoin
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

# Inicializa a variável 'placa' como None
placa = None

# Procura por elementos que contenham a placa
placa_element = soup.find('div', class_='four columns fv input-button')  # Ajuste o seletor conforme necessário

# Verifica se encontrou o elemento da placa
if placa_element:
    placa = placa_element.text.strip()  # Extrai o texto da placa e remove espaços extras

print(f"Placa encontrada: {placa}" if placa else "Nenhuma placa encontrada.")

# Encontra todas as divs com a classe 'subport default listar_anexos'
vistoria_divs = soup.find_all('div', class_='subport default listar_anexos')

# URL base do site para transformar os links relativos em absolutos
base_url = "https://www.hitex.com.br"

# Localiza o contêiner com a classe "tab vistorias"
tab_vistorias = driver.find_element(By.CSS_SELECTOR, 'div.tab.vistorias')

# Encontra todos os botões de expansão dentro do contêiner "tab vistorias"
expand_buttons = tab_vistorias.find_elements(By.CSS_SELECTOR, 'i.icon.expand.icon-chevron-down')

# Número total de vistorias baseado nos botões encontrados dentro de "tab vistorias"
numero_vistorias = len(expand_buttons)
print(f"Total de vistorias encontradas: {numero_vistorias}")

# Itera sobre o número de vistorias, começando em 1 e indo até o número total
for index in range(1, numero_vistorias + 1):  # Começa em 1 e vai até numero_vistorias
    try:
        # Localiza os botões de expansão novamente dentro de "tab vistorias"
        expand_buttons = tab_vistorias.find_elements(By.CSS_SELECTOR, 'i.icon.expand.icon-chevron-down')
        button = expand_buttons[index - 1]  # Ajusta o índice para acessar o botão correto
        
        print(f"Abrindo botão de expansão {index}/{numero_vistorias}")
        
        # Scroll até o botão para garantir que ele esteja visível
        ActionChains(driver).move_to_element(button).perform()
        
        # Clica no botão para expandir
        button.click()
        time.sleep(2)  # Pequena pausa para permitir o carregamento das imagens
        
        # Captura o contêiner da vistoria expandida
        vistoria_container = tab_vistorias.find_elements(By.CSS_SELECTOR, 'div.subport.default.listar_anexos')[index - 1]
        
        # Captura o conteúdo da div 'caption' dentro do contêiner da vistoria
        caption_div = vistoria_container.find_element(By.CSS_SELECTOR, 'div.caption')
        numero, data_hora, nome, telefone = None, None, None, None

        if caption_div:
            caption_text = caption_div.text.strip()
            partes = caption_text.split('#')
            if len(partes) >= 5:
                numero = partes[1].strip()
                data_hora = partes[2].strip()
                nome = partes[3].strip()
                telefone = partes[4].strip()
        
        print(f"Vistoria número: {numero}, Data/Hora: {data_hora}, Nome: {nome}, Telefone: {telefone}")
        
        # Captura os links das imagens dentro do contêiner da vistoria expandida
        links = vistoria_container.find_elements(By.CSS_SELECTOR, 'a.abrir_anexo')
        for link in links:
            print("Link encontrado:", link.get_attribute('href'))
        
        # Localiza o botão de "fechar" (pode ser o mesmo botão com estado alterado)
        close_button = vistoria_container.find_element(By.CSS_SELECTOR, 'i.icon.collapse.icon-chevron-up')
        
        print(f"Fechando botão de expansão {index}/{numero_vistorias}")
        
        # Scroll até o botão para garantir que ele esteja visível
        ActionChains(driver).move_to_element(close_button).perform()
        
        # Clica no botão para fechar
        close_button.click()
        time.sleep(1)  # Pequena pausa para garantir que o fechamento seja processado
        
    except Exception as e:
        print(f"Erro ao processar a vistoria {index}: {e}")



# for vistoria in vistoria_divs:
#     # Captura o conteúdo da div 'caption'
#     caption_div = vistoria.find('div', class_='caption')
    
#     # Inicializa as variáveis
#     numero, data_hora, nome, telefone = None, None, None, None

#     if caption_div:
#         caption_text = caption_div.text.strip()
#         partes = caption_text.split('#')
#         if len(partes) >= 5:
#             numero = partes[1].strip()
#             data_hora = partes[2].strip()
#             nome = partes[3].strip()
#             telefone = partes[4].strip()

#     # Captura o status
#     status_span = vistoria.find('span', class_='label')
#     status = status_span.text.strip() if status_span else "Status não encontrado"

#     # Captura os atributos 'alt' e os links das imagens
#     imagens = []

#     # ➜ Captura imagens dentro de 'dz-image'
#     imagens_div = vistoria.find_all('div', class_='dz-image')
#     for imagem_div in imagens_div:
#         img_tag = imagem_div.find('img')
#         if img_tag:
#             alt_text = img_tag.get('alt', 'Sem descrição')
#             src_link = img_tag.get('src', '')
#             full_src = urljoin(base_url, src_link) if src_link else ''
#             imagens.append({'alt': alt_text, 'src': full_src})

#     # ➜ Captura os links dentro de 'dz-details'
#     detalhes_div = vistoria.find_all('div', class_='dz-details')
#     for detalhe in detalhes_div:
#         links = detalhe.find_all('a')
#         for link in links:
#             href = link.get("href")
#             if href:
#                 full_url = urljoin(base_url, href)
#                 imagens.append({'alt': link.text.strip(), 'src': full_url})

#     # Adiciona as informações capturadas à lista
#     vistorias.append({
#         'numero': numero,
#         'data_hora': data_hora,
#         'nome': nome,
#         'telefone': telefone,
#         'status': status,
#         'imagens': imagens
#     })

# # Exibe as informações capturadas
# for vistoria in vistorias:
#     print(f"Número: {vistoria['numero']}")
#     print(f"Data e Hora: {vistoria['data_hora']}")
#     print(f"Nome: {vistoria['nome']}")
#     print(f"Telefone: {vistoria['telefone']}")
#     print(f"Status: {vistoria['status']}")
#     print("Imagens:")
#     for img in vistoria['imagens']:
#         print(f"  - {img['alt']} ({img['src']})")
#     print("-" * 50)