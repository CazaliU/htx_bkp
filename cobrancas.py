from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from sql import engine, DadosClientes, Lancamentos, Sinistros
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
botoes_ver = driver.find_elements(By.CSS_SELECTOR, '#listar_cobrancas i.icon.icon-info.info_info.info_cobranca')
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
        
        # Captura o status geral da cobrança (exemplo: "VENCIDA!")
        status_geral_tag = soup.find('span', class_='label label-danger label-sm')
        status_geral = status_geral_tag.get_text(strip=True) if status_geral_tag else None

        # Exibe o status geral capturado
        print(f"Status Geral: {status_geral}")
        
        # Localiza a seção 'tab dados'
        tab_dados = soup.find('div', class_='tab dados')
        if tab_dados:
            # Captura os dados da seção 'eight columns' dentro de 'tab dados'
            eight_columns = tab_dados.find('div', class_='eight columns')
            if eight_columns:
                try:
                    # Captura o título da seção (exemplo: "Rateio de Sinistros")
                    titulo_tag = eight_columns.find('h3', class_='form_section')
                    titulo = titulo_tag.get_text(strip=True) if titulo_tag else None
                  
                    # Captura os dados específicos da seção 'eight columns'
                    integrante_tag = eight_columns.find('b', text=re.compile(r'Integrante:'))
                    integrante = integrante_tag.next_sibling.strip() if integrante_tag else None

                    id_nosso_numero_tag = eight_columns.find('b', text=re.compile(r'Id./Nosso Número:'))
                    id_nosso_numero = id_nosso_numero_tag.next_sibling.strip() if id_nosso_numero_tag else None

                    vencimento_tag = eight_columns.find('b', text=re.compile(r'Vencimento:'))
                    vencimento = vencimento_tag.next_sibling.strip() if vencimento_tag else None

                    emissao_tag = eight_columns.find('b', text=re.compile(r'Emissão:'))
                    emissao = emissao_tag.next_sibling.strip() if emissao_tag else None

                    vencimento_original_tag = eight_columns.find('b', text=re.compile(r'Vencimento Original:'))
                    vencimento_original = vencimento_original_tag.next_sibling.strip() if vencimento_original_tag else None

                    parcela_tag = eight_columns.find('b', text=re.compile(r'N° da Parcela:'))
                    parcela = parcela_tag.next_sibling.strip() if parcela_tag else None
                    
                    qtd_parcelas_tag = eight_columns.find('b', text=re.compile(r'Qtd. de Parcelas:'))
                    qtd_parcelas = qtd_parcelas_tag.next_sibling.strip() if qtd_parcelas_tag else None
                    
                    remessado_tag = eight_columns.find('b', text=re.compile(r'Remessado:'))
                    remessado = remessado_tag.next_sibling.strip() if remessado_tag else None

                    banco_tag = eight_columns.find('b', text=re.compile(r'Banco:'))
                    banco = banco_tag.next_sibling.strip() if banco_tag else None

                    conta_tag = eight_columns.find('b', text=re.compile(r'Conta:'))
                    conta = conta_tag.next_sibling.strip() if conta_tag else None

                    status_tag = eight_columns.find('b', text=re.compile(r'Status:'))
                    status = status_tag.find_next('span').get_text(strip=True) if status_tag else None
                    
                    # Localiza o botão com a classe 'icon-chevron-down' dentro da seção 'eight columns'
                    chevron_button = eight_columns.find('i', class_='icon icon-chevron-down')
                    if chevron_button:
                        try:
                            # Localiza o elemento no Selenium usando o seletor CSS
                            chevron_button_element = driver.find_element(By.CSS_SELECTOR, 'div.eight.columns i.icon.icon-chevron-down')

                            # Clica no botão para expandir os dados
                            chevron_button_element.click()
                            time.sleep(2)  # Aguarde o carregamento dos dados adicionais

                            # Extrai o HTML atualizado após o clique
                            html = driver.page_source
                            soup = BeautifulSoup(html, 'html.parser')

                            # Localiza a tabela dentro da seção expandida
                            tabela = eight_columns.find('table', class_='table_simples')
                            if tabela:
                                try:
                                    # Captura o cabeçalho da tabela
                                    cabecalhos = [th.get_text(strip=True) for th in tabela.find_all('th')]
                                    print(f"Cabeçalhos da tabela: {cabecalhos}")

                                    # Captura as linhas da tabela
                                    linhas = tabela.find_all('tr')
                                    dados_tabela = []

                                    for linha in linhas:
                                        colunas = linha.find_all('td')
                                        if colunas:
                                            # Captura os dados de cada coluna
                                            dados_linha = [coluna.get_text(strip=True) for coluna in colunas]
                                            dados_tabela.append(dados_linha)

                                    # Exibe os dados capturados
                                    print("\nDados capturados da tabela:")
                                    for linha in dados_tabela:
                                        print(linha)

                                except Exception as e:
                                    print(f"Erro ao capturar os dados da tabela: {e}")
                            else:
                                print("Tabela 'table_simples' não encontrada.")

                        except Exception as e:
                            print(f"Erro ao clicar no botão para expandir os dados: {e}")
                    else:
                        print("Botão 'icon-chevron-down' não encontrado.")

                    # Exibe os dados capturados da seção 'eight columns'
                    print("\nDados capturados da seção 'eight columns':")
                    print(f"Título: {titulo}")
                    print(f"Integrante: {integrante}")
                    print(f"Id./Nosso Número: {id_nosso_numero}")
                    print(f"Vencimento: {vencimento}")
                    print(f"Emissão: {emissao}")
                    print(f"Vencimento Original: {vencimento_original}")
                    print(f"N° da Parcela: {parcela}")
                    print(f"Qtd. de Parcelas: {qtd_parcelas}")
                    print(f"Remessado: {remessado}")
                    print(f"Banco: {banco}")
                    print(f"Conta: {conta}")
                    print(f"Status: {status}")

                except Exception as e:
                    print(f"Erro ao capturar os dados da seção 'eight columns': {e}")

            # Captura os dados da seção 'four columns' dentro de 'tab dados'
            four_columns = tab_dados.find('div', class_='four columns')
            if four_columns:
                try:
                    # Captura o valor (exemplo: R$ 9.722,75)
                    valor_tag = four_columns.find('h3', class_='form_section')
                    valor = valor_tag.find('b').get_text(strip=True) if valor_tag else None

                    # Captura o texto de referência (exemplo: Boleto referente Rateio Mensal)
                    referencia_tag = four_columns.find('div', class_='well')
                    referencia = referencia_tag.get_text(strip=True) if referencia_tag else None

                    # Exibe os dados capturados da seção 'four columns'
                    print("\nDados capturados da seção 'four columns':")
                    print(f"Valor: {valor}")
                    print(f"Referência: {referencia}")

                except Exception as e:
                    print(f"Erro ao capturar os dados da seção 'four columns': {e}")
        else:
            print("Seção 'tab dados' não encontrada.")
        
        # fecha modal
        pyautogui.click(x=153, y=656)
        time.sleep(1)
        
    except Exception as e:
      # fecha modal
      pyautogui.click(x=153, y=656)
      print(f"Erro ao processar cobranca {index}: {e}")

# Fecha o navegador
driver.quit()