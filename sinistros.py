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

remote_folder = "/var/www/imagens_sinistros/"

def process_images_and_save(session, cliente_id, veiculo_1, veiculo_2, veiculo_3, estado, cidade, tipo, codigo, responsabilidade, descricao_privada, descricao_publica, data_ocorrencia, status, image_links, nomes_imagens):
    local_folder = f"temp_sinistro_{codigo}"  # Pasta temporária para armazenar as imagens
    remote_paths = []

    try:
        # Cria a pasta temporária
        if not os.path.exists(local_folder):
            os.makedirs(local_folder)

        # Baixa todas as imagens localmente e renomeia
        for href, novo_nome in image_links:
            local_path = os.path.join(local_folder, novo_nome)

            # Baixa a imagem
            response = requests.get(href, stream=True)
            if response.status_code == 200:
                with open(local_path, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"Imagem baixada e renomeada: {local_path}")  # Agora o nome correto será exibido
            else:
                print(f"Erro ao baixar a imagem: {href}")

        # Envia todas as imagens para o servidor
        transport = paramiko.Transport((host_ssh, port_ssh))
        transport.connect(username=username_ssh, password=password_ssh)
        sftp = paramiko.SFTPClient.from_transport(transport)

        for file_name in os.listdir(local_folder):
            local_path = os.path.join(local_folder, file_name)
            remote_path = os.path.join(remote_folder, file_name)
            sftp.put(local_path, remote_path)
            remote_paths.append(remote_path)  # Salva o caminho completo no banco
            print(f"Imagem enviada para o servidor: {remote_path}")

        sftp.close()
        transport.close()

        # Salva os dados do sinistro no banco de dados
        novo_sinistro = Sinistros(
            si_cliente_id=cliente_id,
            si_veiculo_1=veiculo_1,
            si_veiculo_2=veiculo_2,
            si_veiculo_3=veiculo_3,
            si_estado=estado,
            si_cidade=cidade,
            si_tipo=tipo,
            si_codigo=codigo,
            si_responsabilidade=responsabilidade,
            si_descricao_privada=descricao_privada,
            si_descricao_publica=descricao_publica,
            si_data_ocorrencia=data_ocorrencia,
            si_status=status,
            si_caminho_anexos=remote_paths  # Salva os caminhos completos no banco
        )
        session.add(novo_sinistro)
        session.commit()
        print("Dados do sinistro e caminhos das imagens salvos no banco de dados com sucesso!")

    except Exception as e:
        print(f"Erro ao processar as imagens: {e}")
        session.rollback()
    finally:
        # Remove a pasta temporária e os arquivos locais
        if os.path.exists(local_folder):
            try:
                print(f"Removendo a pasta temporária: {local_folder}")
                shutil.rmtree(local_folder)
                print("Pasta temporária removida com sucesso.")
            except Exception as e:
                print(f"Erro ao remover a pasta temporária: {e}")


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

time.sleep(15)

# Espera até que o modal esteja visível
modal_selector = 'modal-body'  # Substitua pelo seletor que corresponde ao modal
driver.implicitly_wait(10)  # Espera implícita para o modal

# Localiza todos os botões "VER" na página
botoes_ver = driver.find_elements(By.CSS_SELECTOR, 'a.info_sinistro')
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
        
        # Extrai o HTML da página
        html = driver.page_source
        
        # Analisa o HTML com BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # --- DADOS DO SINISTRO ---
        sinistro_tab = soup.find('div', {'class': 'ltab', 'id': 'ldados'})
        if sinistro_tab:
            print("=== DADOS DO SINISTRO ===")
            integrante_nome = None
            veiculos = []
            si_veiculo_1 = None
            si_veiculo_2 = None
            si_veiculo_3 = None
            estado = None
            cidade = None
            tipo = None
            codigo = None
            responsabilidade = None
            descricao_privada = None
            descricao_publica = None

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
                    if campo == "Integrante:":
                        integrante_nome = b_tag.next_sibling.strip() if b_tag.next_sibling else None
                        print(f"{campo} {integrante_nome}")
                    elif campo == "Veículos:":
                        sibling = b_tag.next_sibling
                        while sibling:
                            if sibling.name == 'span' and sibling.find('b'):
                                veiculos.append(sibling.find('b').get_text(strip=True))
                            elif sibling.string and sibling.string.strip() != "#" and sibling.string.strip():
                                veiculos.append(sibling.string.strip())
                            sibling = sibling.next_sibling
                        print(f"{campo} {', '.join(veiculos)}")

                        # Filtra valores inválidos como '#'
                        veiculos = [placa for placa in veiculos if placa != "#"]

                        # Divide as placas em até 3 partes
                        si_veiculo_1 = veiculos[0] if len(veiculos) > 0 else None
                        si_veiculo_2 = veiculos[1] if len(veiculos) > 1 else None
                        si_veiculo_3 = veiculos[2] if len(veiculos) > 2 else None
                    elif campo == "Data de Ocorrência:":
                        data_ocorrencia = b_tag.next_sibling.strip() if b_tag.next_sibling else None
                        print(f"{campo} {data_ocorrencia}")
                    elif campo == "Status:":
                        status = b_tag.next_sibling.strip() if b_tag.next_sibling else None
                        print(f"{campo} {status}")
                    elif campo == "Estado:":
                        estado = b_tag.next_sibling.strip() if b_tag.next_sibling else None
                        print(f"{campo} {estado}")
                    elif campo == "Cidade:":
                        cidade = b_tag.next_sibling.strip() if b_tag.next_sibling else None
                        print(f"{campo} {cidade}")
                    elif campo == "Tipo:":
                        tipo = b_tag.next_sibling.strip() if b_tag.next_sibling else None
                        print(f"{campo} {tipo}")
                    elif campo == "Código:":
                        label = b_tag.find_next('span', class_='label')  # Busca o próximo elemento <span> com a classe 'label'
                        raw_codigo = label.get_text(strip=True) if label else None  # Captura o texto bruto
                        codigo = re.sub(r'\D', '', raw_codigo) if raw_codigo else None  # Remove todos os caracteres não numéricos
                        print(f"{campo} {codigo}")
                    elif campo == "Responsabilidade:":
                        responsabilidade = b_tag.next_sibling.strip() if b_tag.next_sibling else None
                        print(f"{campo} {responsabilidade}")


            wells = sinistro_tab.find_all('div', class_='well')
            descricao_privada = wells[0].get_text(strip=True) if len(wells) > 0 else None
            descricao_publica = wells[1].get_text(strip=True) if len(wells) > 1 else None

            if integrante_nome:
                try:
                    Session = sessionmaker(bind=engine)
                    session = Session()
                    cliente = session.query(DadosClientes).filter(DadosClientes.razao_social.ilike(f"%{integrante_nome}%")).first()
                    if cliente:
                        print(f"ID do cliente encontrado: {cliente.id}")
                    else:
                        print(f"Nenhum cliente encontrado para o integrante: {integrante_nome}")
                        pyautogui.click(x=1756, y=557)
                        time.sleep(1)
                        continue
                except Exception as e:
                    print(f"Erro ao buscar o cliente no banco de dados: {e}")
                finally:
                    session.close()

        else:
            print("Dados do sinistro não encontrados.")


        # Localiza a aba anexos dentro do modal
        aba_anexos = driver.find_element(By.CSS_SELECTOR, 'li[data-id="anexos"]')
        aba_anexos.click()
        time.sleep(2)  # Aguarde o carregamento da aba
        
        # Extrai o HTML da página
        html = driver.page_source
        # Analisa o HTML com BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        # URL base do site para transformar os links relativos em absolutos
        base_url = "https://www.hitex.com.br"
        
        # Localiza o contêiner com os anexos
        anexos_container = soup.find('div', class_='anexos_previews')

        # Captura os links das imagens dentro do contêiner de anexos
        if anexos_container:
            links = anexos_container.find_all('a', class_='abrir_anexo')
            imagens = []
            nomes_imagens = []

            for link in links:
                href = urljoin(base_url, link['href'])  # Gera o link completo
                if href:
                    # Extrai o identificador do parâmetro "a="
                    identificador = re.search(r'a=([^&]+)', href).group(1)  # Captura o valor após "a="
                    
                    # Verifica se o identificador já contém "uni_"
                    if not identificador.startswith("uni_"):
                        novo_nome = f"uni_{identificador}"  # Adiciona "uni_" apenas se não estiver presente
                    else:
                        novo_nome = identificador  # Usa o identificador diretamente
                    
                    # Concatena o caminho do servidor com o nome da imagem
                    caminho_completo = os.path.join(remote_folder, novo_nome)
                    
                    imagens.append((href, novo_nome))  # Armazena o link completo e o novo nome
                    nomes_imagens.append(caminho_completo)  # Salva o caminho completo no banco de dados
                    
                    print("Link completo:", href)
                    print("Novo nome da imagem:", novo_nome)
                    print("Caminho completo para o banco de dados:", caminho_completo)

            # Processa as imagens e salva os dados no banco de dados
            if cliente:
                process_images_and_save(
                    session=session,
                    cliente_id=cliente.id,
                    veiculo_1=si_veiculo_1,
                    veiculo_2=si_veiculo_2,
                    veiculo_3=si_veiculo_3,
                    estado=estado,
                    cidade=cidade,
                    tipo=tipo,
                    codigo=codigo,
                    responsabilidade=responsabilidade,
                    descricao_privada=descricao_privada,
                    descricao_publica=descricao_publica,
                    data_ocorrencia=data_ocorrencia,
                    status=status,
                    image_links=imagens,  # Passa os links completos e os novos nomes
                    nomes_imagens=nomes_imagens  # Passa os caminhos completos para salvar no banco
                )
        else:
            print("Nenhum anexo encontrado.")
        
        # fecha modal
        pyautogui.click(x=1756, y=557)
            
    except Exception as e:
      print(f"Erro ao processar sinistro {index}: {e}")

# Fecha o navegador
driver.quit()