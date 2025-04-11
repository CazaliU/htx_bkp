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

# Função para enviar imagens diretamente para o servidor
def upload_image_to_server(url, remote_folder, identificador):
    try:
        # Baixa o conteúdo da imagem
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            # Conecta ao servidor via SFTP
            transport = paramiko.Transport((host_ssh, port_ssh))
            transport.connect(username=username_ssh, password=password_ssh)
            sftp = paramiko.SFTPClient.from_transport(transport)

            # Define o nome do arquivo com o identificador
            original_file_name = url.split('=')[-1]  # Extrai o nome original do arquivo do URL
            file_extension = os.path.splitext(original_file_name)[-1]  # Obtém a extensão do arquivo
            new_file_name = f"{identificador}_{original_file_name}"  # Adiciona o identificador ao nome do arquivo

            # Define o caminho remoto para salvar a imagem
            remote_path = os.path.join(remote_folder, new_file_name)  # Usa os.path.join para evitar barras duplicadas

            with sftp.file(remote_path, 'wb') as remote_file:
                for chunk in response.iter_content(1024):
                    remote_file.write(chunk)

            print(f"Imagem enviada para o servidor: {remote_path}")
            sftp.close()
            transport.close()
            return remote_path
        else:
            print(f"Erro ao baixar a imagem: {url}")
            return None
    except Exception as e:
        print(f"Erro ao enviar a imagem para o servidor: {e}")
        return None

# Função para salvar os caminhos no banco de dados
def save_to_database(session, veiculo_id, numero, status, data_hora, nome, telefone, remote_paths):
    try:
        print(f"Remote paths antes da conversão: {remote_paths}")

        # Substitui strings vazias por None
        numero = numero if numero.strip() else None
        status = status if status.strip() else None
        data_hora = data_hora if data_hora.strip() else None
        nome = nome if nome.strip() else None
        telefone = telefone if telefone.strip() else None

        # Cria um único registro para a vistoria
        nova_vistoria = VistoriaImagens(
            vi_veiculo_id=int(veiculo_id),  # Certifique-se de que é um inteiro
            vi_identificador=numero,  # Substitui string vazia por None
            vi_status=status,  # Substitui string vazia por None
            vi_data_hora=data_hora,  # Substitui string vazia por None
            vi_nome=nome,  # Substitui string vazia por None
            vi_telefone=telefone,  # Substitui string vazia por None
            vi_caminho=remote_paths  # Passa a lista diretamente
        )
        session.add(nova_vistoria)
        session.commit()
        print("Caminhos das imagens salvos no banco de dados com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar no banco de dados: {e}")
        session.rollback()

# Processa as imagens encontradas
def process_images(session, veiculo_id, numero, status, data_hora, nome, telefone, image_links):
    local_folder = f"temp_vistoria_{numero}"  # Pasta temporária para armazenar as imagens
    remote_paths = []

    try:
        # Cria a pasta temporária
        if not os.path.exists(local_folder):
            os.makedirs(local_folder)

        # Baixa todas as imagens localmente
        for link in image_links:
            file_name = f"{numero}_{link.split('=')[-1]}"  # Renomeia o arquivo com o identificador
            local_path = os.path.join(local_folder, file_name)

            # Baixa a imagem
            response = requests.get(link, stream=True)
            if response.status_code == 200:
                with open(local_path, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"Imagem baixada: {local_path}")
            else:
                print(f"Erro ao baixar a imagem: {link}")

        # Envia todas as imagens para o servidor
        transport = paramiko.Transport((host_ssh, port_ssh))
        transport.connect(username=username_ssh, password=password_ssh)
        sftp = paramiko.SFTPClient.from_transport(transport)

        for file_name in os.listdir(local_folder):
            local_path = os.path.join(local_folder, file_name)
            remote_path = os.path.join(remote_folder, file_name)
            sftp.put(local_path, remote_path)
            remote_paths.append(remote_path)
            print(f"Imagem enviada para o servidor: {remote_path}")

        sftp.close()
        transport.close()

        # Salva os caminhos no banco de dados
        if remote_paths:
            save_to_database(session, veiculo_id, numero, status, data_hora, nome, telefone, remote_paths)

    except Exception as e:
        print(f"Erro ao processar as imagens: {e}")
    finally:
        # Remove a pasta temporária e os arquivos locais
        if os.path.exists(local_folder):
            shutil.rmtree(local_folder)



# Obter as credenciais a partir das variáveis de ambiente
username = os.getenv('APP_USERNAME')
password = os.getenv('APP_PASSWORD')

# Obter as credenciais do arquivo .env
host_ssh = os.getenv('HOST_SSH')
port_ssh = int(os.getenv('PORT_SSH'))  # Converte para inteiro
username_ssh = os.getenv('USERNAME_SSH')
password_ssh = os.getenv('PASSWORD_SSH')
remote_folder = "/var/www/imagens_vistorias/"

# Configura o caminho para o ChromeDriver
chrome_driver_path = r'C:\Users\rafae\Downloads\chromedriver-win64\chromedriver.exe'  # Caminho atualizado

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

# Localiza todos os botões "VER" na página
botoes_ver = driver.find_elements(By.CSS_SELECTOR, 'a.bold.info_veiculo')
print(f"Total de botões encontrados: {len(botoes_ver)}")

# Itera sobre os botões
for index, botao in enumerate(botoes_ver):
    try:
        print(f"Acessando botão {index + 1} de {len(botoes_ver)}")

        # Scroll até o botão para garantir que ele esteja visível
        ActionChains(driver).move_to_element(botao).perform()
        
        # Clica no botão para abrir o modal
        botao.click()
        time.sleep(2)  # Aguarde o modal carregar
        
        # Localiza a aba vistorias dentro do modal
        aba_vistorias = driver.find_element(By.CSS_SELECTOR, 'li[data-id="vistorias"]')
        aba_vistorias.click()
        time.sleep(2)  # Aguarde o carregamento da aba

        # Extrai o HTML da página
        html = driver.page_source

        # Analisa o HTML com BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Inicializa a variável 'placa' como None
        placa = None
        veiculo_id = None

        # Procura por elementos que contenham a placa
        placa_element = soup.find('div', class_='four columns fv input-button')  # Ajuste o seletor conforme necessário

        # Verifica se encontrou o elemento da placa
        if placa_element:
            placa_text = placa_element.text.strip()  # Extrai o texto e remove espaços extras
            if "Placa:" in placa_text:
                placa = placa_text.replace("Placa:", "").strip()  # Remove o prefixo "Placa:" e espaços extras
                
                # Cria uma sessão para interagir com o banco de dados
                Session = sessionmaker(bind=engine)
                session = Session()
                
                try:
                    # Consulta a tabela 'veiculos' para verificar se a placa existe
                    veiculo = session.query(Veiculos).filter(
                        Veiculos.ve_placa1.ilike(placa) # Verifica na coluna ve_placa1
                    ).first()

                    if veiculo:
                        print(f"Placa encontrada no banco de dados! ID do veículo: {veiculo.ve_id}")
                        veiculo_id = veiculo.ve_id  # Armazena o ID do veículo
                        
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

                        vistorias = []
                        
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
                                numero, data_hora, nome, telefone, status = None, None, None, None, None

                                if caption_div:
                                    caption_text = caption_div.text.strip()
                                    partes = caption_text.split('#')
                                    if len(partes) >= 5:
                                        numero = partes[1].strip()
                                        data_hora = partes[2].strip()
                                        nome = partes[3].strip()
                                        telefone = partes[4].strip()

                                # Captura o status da vistoria
                                try:
                                    status_span = vistoria_container.find_element(By.CSS_SELECTOR, 'span.label')
                                    status = status_span.text.strip()  # Extrai o texto do status
                                except Exception as e:
                                    print(f"Erro ao capturar o status da vistoria {numero}: {e}")

                                print(f"Vistoria número: {numero}, Data/Hora: {data_hora}, Nome: {nome}, Telefone: {telefone}, Status: {status}")

                                # Captura os links das imagens dentro do contêiner da vistoria expandida
                                links = vistoria_container.find_elements(By.CSS_SELECTOR, 'a.abrir_anexo')
                                imagens = [link.get_attribute('href') for link in links]
                                for link in imagens:
                                    print("Link encontrado:", link)

                                process_images(
                                    session=session,
                                    veiculo_id=veiculo_id,
                                    numero=numero,
                                    status=status,
                                    data_hora=data_hora,
                                    nome=nome,
                                    telefone=telefone,
                                    image_links=imagens
                                )
                                
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
                        
                    else:
                        print("Placa não encontrada no banco de dados.")
                        # colocar para sair do loop
                except Exception as e:
                    print(f"Erro ao consultar o banco de dados: {e}")
                finally:
                    # Fecha a sessão
                    session.close()
            else:
                print("Nenhuma placa foi encontrada no web scraping.")
                #conitnuar
                
            pyautogui.click(x=1756, y=557)  # Clica fora do modal para fechá-lo
            
    except Exception as e:
        print(f"Erro ao processar o botão {index + 1}: {e}")
                
# Fecha o navegador
driver.quit()