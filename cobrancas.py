from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from sql import engine, DadosClientes, Cobrancas
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

while True:
    try:      
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
              
              status_geral = None
              titulo = None
              integrante = None
              id_nosso_numero = None
              vencimento = None
              emissao = None
              vencimento_original = None
              parcela = None
              qtd_parcelas = None
              remessado = None
              banco = None
              conta = None
              status = None
              protesto_automatico = None
              dias_protestar = None
              valor = None
              referencia = None
              ultima_consulta = None
              dados_tabela = []  # Lista para armazenar os dados da tabela expandida
              dados_historico = []  # Lista para armazenar os dados da tabela de histórico
              
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
                          
                          protesto_automatico_tag = eight_columns.find('b', text=re.compile(r'Protesto Automático:'))
                          protesto_automatico = protesto_automatico_tag.next_sibling.strip() if protesto_automatico_tag else None

                          dias_protestar_tag = eight_columns.find('b', text=re.compile(r'Dias p/ Protestar:'))
                          dias_protestar = dias_protestar_tag.next_sibling.strip() if dias_protestar_tag else None

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
                          print(f"Protesto Automático: {protesto_automatico}")
                          print(f"Dias p/ Protestar: {dias_protestar}")

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
                  
              if integrante:    
                try:
                  Session = sessionmaker(bind=engine)
                  session = Session()
                  
                  # Verifica se o cliente existe
                  cliente = session.query(DadosClientes).filter(DadosClientes.razao_social.ilike(f"%{integrante}%")).first()
                  if cliente:
                      print(f"ID do cliente encontrado: {cliente.id}")
                  else:
                    print(f"Nenhum cliente encontrado para o integrante: {integrante}")
                    pyautogui.click(x=153, y=656)
                    time.sleep(1)
                    continue
                except Exception as e:
                    print(f"Erro ao buscar o cliente no banco de dados: {e}")
                finally:
                    session.close()
            
              if integrante:
                  # Localiza a aba histórico dentro do modal
                  aba_historico = driver.find_element(By.CSS_SELECTOR, 'li[data-id="historico"]')
                  aba_historico.click()
                  time.sleep(2)  # Aguarde o carregamento da aba

                  # Extrai o HTML da página
                  html = driver.page_source
                  # Analisa o HTML com BeautifulSoup
                  soup = BeautifulSoup(html, 'html.parser')

                  # Localiza a seção 'tab historico'
                  tab_historico = soup.find('div', class_='tab historico')
                  if tab_historico:
                      try:
                          print("\nDados capturados da aba histórico:")
                          # Captura a última consulta
                          ultima_consulta_tag = tab_historico.find('b', text=re.compile(r'Última Consulta:'))
                          ultima_consulta = ultima_consulta_tag.next_sibling.strip() if ultima_consulta_tag else None
                          print(f"Última Consulta: {ultima_consulta}")

                          # Localiza a tabela de histórico de interações
                          tabela_historico = tab_historico.find('table', class_='table_simples')
                          if tabela_historico:
                              try:
                                  # Captura o cabeçalho da tabela
                                  cabecalhos = [th.get_text(strip=True) for th in tabela_historico.find_all('th')]
                                  print(f"Cabeçalhos da tabela: {cabecalhos}")

                                  # Captura as linhas da tabela
                                  linhas = tabela_historico.find_all('tr')
                                  dados_historico = []

                                  for linha in linhas:
                                      colunas = linha.find_all('td')
                                      if colunas:
                                          # Captura os dados de cada coluna
                                          dados_linha = [coluna.get_text(strip=True) for coluna in colunas]
                                          dados_historico.append(dados_linha)

                                  # Exibe os dados capturados
                                  print("\nDados capturados da tabela de histórico:")
                                  for linha in dados_historico:
                                      print(linha)

                              except Exception as e:
                                  print(f"Erro ao capturar os dados da tabela de histórico: {e}")
                          else:
                              print("Tabela de histórico não encontrada na aba histórico.")

                      except Exception as e:
                          print(f"Erro ao capturar os dados da aba histórico: {e}")
                  else:
                      print("Aba histórico não encontrada.")
                      
              if id_nosso_numero:  # Verifica se o id_nosso_numero foi capturado
                  try:
                      Session = sessionmaker(bind=engine)
                      session = Session()

                      # Verifica se o id_nosso_numero já existe na tabela 'cobrancas'
                      cobranca_existente = session.query(Cobrancas).filter(Cobrancas.co_id_nosso_numero == id_nosso_numero).first()
                      if cobranca_existente:
                          print(f"O ID/Nosso Número '{id_nosso_numero}' já existe na tabela 'cobrancas'. Ignorando inserção.")
                      else:
                          # Insere os dados na tabela 'cobrancas'
                          nova_cobranca = Cobrancas(
                            co_status_geral=str(status_geral) if status_geral else None,
                            co_titulo=str(titulo) if titulo else None,
                            co_integrante=str(integrante) if integrante else None,
                            co_id_nosso_numero=str(id_nosso_numero) if id_nosso_numero else None,
                            co_vencimento=str(vencimento) if vencimento else None,
                            co_emissao=str(emissao) if emissao else None,
                            co_vencimento_original=str(vencimento_original) if vencimento_original else None,
                            co_parcela=str(parcela) if parcela else None,
                            co_qtd_parcelas=str(qtd_parcelas) if qtd_parcelas else None,
                            co_protesto_automatico=str(protesto_automatico) if protesto_automatico else None,
                            co_dias_protestar=str(dias_protestar) if dias_protestar else None,
                            co_banco=str(banco) if banco else None,
                            co_conta=str(conta) if conta else None,
                            co_remessado=str(remessado) if remessado else None,
                            co_status=str(status) if status else None,
                            co_valor=str(valor) if valor else None,
                            co_referencia=str(referencia) if referencia else None,
                            co_dados_complementares=dados_tabela if dados_tabela else None,  # Lista ou None
                            co_historico_ultima_consulta=str(ultima_consulta) if ultima_consulta else None,
                            co_historico=dados_historico if dados_historico else None,  # Lista ou None
                            co_cliente_id=cliente.id if cliente else None,
                          )
                          session.add(nova_cobranca)
                          session.commit()
                          print(f"Nova cobrança com ID/Nosso Número '{id_nosso_numero}' inserida com sucesso.")

                  except Exception as e:
                      print(f"Erro ao verificar/inserir cobrança: {e}")
                  finally:
                      session.close()
              
              # fecha modal
              pyautogui.click(x=153, y=656)
              time.sleep(1)
              
          except Exception as e:
            # fecha modal
            pyautogui.click(x=153, y=656)
            print(f"Erro ao processar cobranca {index}: {e}")
            
      # Verifica se o botão "Próxima" está habilitado
      botao_proxima = driver.find_element(By.ID, 'listar_cobrancas_next')
      if "disabled" in botao_proxima.get_attribute("class"):
          print("Botão 'Próxima' está desabilitado. Fim da navegação.")
          break  # Sai do loop se não houver mais páginas
      
      # Fecha qualquer modal que possa estar bloqueando o botão
      pyautogui.click(x=153, y=656)
      time.sleep(4)
  
      # Clica no botão "Próxima" para ir para a próxima página
      driver.execute_script("arguments[0].scrollIntoView();", botao_proxima)
      time.sleep(1)
      botao_proxima.click()
      time.sleep(3)
            
    except Exception as e:
        print(f"Erro durante a navegação: {e}")
        break

# Fecha o navegador
driver.quit()