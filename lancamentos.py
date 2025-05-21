from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from sql import engine, DadosClientes, Sinistros
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
import re
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

# Localiza todos os botões dentro da tabela com id "movimento_pendente"
botoes_ver = driver.find_elements(By.CSS_SELECTOR, '#movimento_pendente i.icon.icon-info.info_info.info_movimento')
print(f"Total de botões encontrados na tabela 'movimento_pendente': {len(botoes_ver)}")

# Itera sobre os botões encontrados
for index, botao in enumerate(botoes_ver):
    try:
        # Fecha o modal antes de iniciar a próxima iteração (caso esteja aberto)
        pyautogui.click(x=153, y=656)
        time.sleep(1)
        
        print(f"Acessando botão {index + 1} de {len(botoes_ver)}")

        # Scroll até o botão para garantir que ele esteja visível
        botao = botoes_ver[index]
        ActionChains(driver).move_to_element(botao).perform()

        # Clica no botão
        botao.click()
        time.sleep(2)  # Aguarde o modal carregar ou a ação ser concluída

        # Extrai o HTML da página após clicar no botão
        html = driver.page_source

        # Analisa o HTML com BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        valor_debito_credito = None
        conta = None
        situacao = None
        data = None
        compensacao = None
        tipo = None
        referente = None
        integrante = None
        sinistro = None
        veiculo = None
        valor = None
        referencia = None

        # Localiza a seção 'tab dados'
        tab_dados = soup.find('div', class_='tab dados')
        if tab_dados:
            
            # Captura os dados da seção 'eight columns' dentro de 'tab dados'
            eight_columns = tab_dados.find('div', class_='eight columns')
            if eight_columns:
                try:
                    
                    # Captura o valor de débito ou crédito
                    valor_debito_credito_tag = eight_columns.find('h3', class_='form_section')
                    if valor_debito_credito_tag:
                        valor_debito_credito = valor_debito_credito_tag.get_text(strip=True)
                    else:
                        valor_debito_credito = None
                        
                    conta_tag = eight_columns.find('b', text=re.compile(r'Conta:'))
                    conta = conta_tag.next_sibling.strip() if conta_tag else None

                    situacao_tag = eight_columns.find('b', text=re.compile(r'Situação:'))
                    situacao = situacao_tag.find_next('span').get_text(strip=True) if situacao_tag else None

                    data_tag = eight_columns.find('b', text=re.compile(r'Data:'))
                    data = data_tag.next_sibling.strip() if data_tag else None

                    compensacao_tag = eight_columns.find('b', text=re.compile(r'Compensação:'))
                    compensacao = compensacao_tag.next_sibling.strip() if compensacao_tag else None

                    tipo_tag = eight_columns.find('b', text=re.compile(r'Tipo:'))
                    tipo = tipo_tag.next_sibling.strip() if tipo_tag else None

                    referente_tag = eight_columns.find('b', text=re.compile(r'Referente:'))
                    referente = referente_tag.next_sibling.strip() if referente_tag else None

                    integrante_tag = eight_columns.find('b', text=re.compile(r'Integrante:'))
                    integrante = integrante_tag.find_next('span').get_text(strip=True) if integrante_tag else None
                    
                    # Captura o campo Sinistro
                    sinistro_tag = eight_columns.find('b', text=re.compile(r'Sinistro:'))
                    sinistro = sinistro_tag.find_next('span').get_text(strip=True) if sinistro_tag else None

                    # Captura o campo Veículo
                    veiculo_tag = eight_columns.find('b', text=re.compile(r'Veículo:'))
                    veiculo = veiculo_tag.next_sibling.strip() if veiculo_tag else None

                    # Exibe os valores capturados
                    print("\nDados capturados da seção 'eight columns':")
                    print(f"Valor (Débito/Crédito): {valor_debito_credito}")
                    print(f"Conta: {conta}")
                    print(f"Situação: {situacao}")
                    print(f"Data: {data}")
                    print(f"Compensação: {compensacao}")
                    print(f"Tipo: {tipo}")
                    print(f"Referente: {referente}")
                    print(f"Integrante: {integrante}")
                    print(f"Sinistro: {sinistro}")
                    print(f"Veículo: {veiculo}")
                     
                except Exception as e:
                    print(f"Erro ao capturar os dados da seção 'eight columns': {e}")
            else:
                print("Seção 'eight columns' não encontrada dentro de 'tab dados'.")

            # Captura os dados da seção 'four columns' dentro de 'tab dados'
            four_columns = tab_dados.find('div', class_='four columns')
            if four_columns:
                # Captura o valor (exemplo: R$ 4.114,81)
                valor_tag = four_columns.find('h3', class_='form_section')
                if valor_tag:
                    valor_b = valor_tag.find('b')
                    valor = valor_b.get_text(strip=True) if valor_b else None
                else:
                    valor = None

                # Captura o texto de referência (exemplo: REF PARTICIPAÇOES A SEREM GERADAS)
                referencia_tag = four_columns.find('div', class_='well')
                referencia = referencia_tag.get_text(strip=True) if referencia_tag else None

                # Exibe os dados capturados
                print("\nDados da seção 'four columns' dentro de 'tab dados':")
                print(f"Valor: {valor}")
                print(f"Referência: {referencia}")
        else:
            print("Seção 'tab dados' não encontrada.")

        if integrante or sinistro:
            try:
                # Cria uma sessão com o banco de dados
                Session = sessionmaker(bind=engine)
                session = Session()

                if integrante:
                    # Verifica se o cliente existe no banco de dados pelo nome do integrante
                    cliente = session.query(DadosClientes).filter(DadosClientes.razao_social.ilike(f"%{integrante}%")).first()
                    if cliente:
                        print(f"ID do cliente encontrado: {cliente.id}")
                    else:
                        print(f"Cliente com o nome '{integrante}' não encontrado no banco de dados.")
                        continue
                elif sinistro:
                    # Extrai os números dentro dos colchetes usando regex
                    sinistro_codigo_match = re.search(r'\[(\d+)/(\d+)-(\d+)\]', sinistro)
                    if sinistro_codigo_match:
                        # Concatena os grupos capturados e converte para inteiro
                        sinistro_codigo = int(f"{sinistro_codigo_match.group(1)}{sinistro_codigo_match.group(2)}{sinistro_codigo_match.group(3)}")
                        print(f"Código do sinistro extraído e convertido: {sinistro_codigo}")

                        # Verifica se o sinistro existe no banco de dados
                        sinistro_obj = session.query(Sinistros).filter(Sinistros.si_codigo == sinistro_codigo).first()
                        if sinistro_obj:
                            print(f"Sinistro encontrado: {sinistro_obj.si_codigo}")
                        else:
                            print(f"Sinistro com o código '{sinistro_codigo}' não encontrado no banco de dados.")
                    else:
                        print(f"Não foi possível extrair o código do sinistro de '{sinistro}'.")
                        continue

            except Exception as e:
                print(f"Erro ao consultar o banco de dados: {e}")
            finally:
                # Fecha a sessão
                session.close()
                    
        pyautogui.click(x=153, y=656) 
        time.sleep(1)

    except Exception as e:
        # fecha modal
        pyautogui.click(x=153, y=656)
        print(f"Erro ao processar lancamento {index}: {e}")

# Fecha o navegador
driver.quit()