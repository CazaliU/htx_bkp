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

    # Encontrar todos os elementos com a classe 'twelve columns fv', 'six columns fv', 'four columns fv', 'four columns fv input-button'
    elementos = soup.find_all('div', class_=['twelve columns fv', 'six columns fv', 'four columns fv', 'four columns fv input-button', 'twelve columns well branco'])
    
    integrante = None
    # tipo = None
    # especie = None
    composicao = None
    cod_fipe = None
    valor_principal = None
    agregado = None
    indice_participacao = None
    estado_grupo = 'Grande Oeste'

    for elemento in elementos:
        texto = elemento.text.strip()
        if texto.startswith("Integrante:"):
            integrante = texto.replace("Integrante:", "").strip()
        # elif texto.startswith("Tipo:"):
        #     tipo = texto.replace("Tipo:", "").strip()
        # elif texto.startswith("Espécie:"):
        #     especie = texto.replace("Espécie:", "").strip()
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
        "espécie": [],
        "tipo": [],
        "carroceria": [],
        "Cap. Max. Carga": [],
        "Peso Bruto Total": [],
        "Cap. Max. Tração": [],
        "N°. Motor": [],
        "potência": [],
        "lotação": [],
        "eixos": [],
        "Nº. CRV": [],
        "Nº. Seg. CLA": [],
        "Observações": [],
        "rastreadores": [],
        "bloqueadores": [],
        "Última Vistoria": [],
        "monitoramento": [],
        "Anotações de Controle:": []
    }


    # Percorre todos os elementos para capturar as informações
    for elemento in elementos:
        texto = elemento.text.strip()
        if texto.startswith("Cap. Max. Carga:"):
            cap_max_carga = texto.replace("Cap. Max. Carga:", "").strip()
            dados_veiculo["Cap. Max. Carga"].append(cap_max_carga)
        elif texto.startswith("Peso Bruto Total:"):
            peso_bruto_total = texto.replace("Peso Bruto Total:", "").strip()
            dados_veiculo["Peso Bruto Total"].append(peso_bruto_total)
        elif texto.startswith("Cap. Max. Tração:"):
            cap_max_tracao = texto.replace("Cap. Max. Tração:", "").strip()
            dados_veiculo["Cap. Max. Tração"].append(cap_max_tracao)
        elif texto.startswith("N°. Motor:"):
            numero_motor = texto.replace("N°. Motor:", "").strip()
            dados_veiculo["N°. Motor"].append(numero_motor)
        elif texto.startswith("Nº. CRV:"):
            numero_crv = texto.replace("Nº. CRV:", "").strip()
            dados_veiculo["Nº. CRV"].append(numero_crv)
        elif texto.startswith("Nº. Seg. CLA:"):
            numero_seg_cla = texto.replace("Nº. Seg. CLA:", "").strip()
            dados_veiculo["Nº. Seg. CLA"].append(numero_seg_cla)
        elif texto.startswith("Observações:"):
            observacoes = texto.replace("Observações:", "").strip()
            dados_veiculo["Observações"].append(observacoes)
        elif texto.startswith("Rastreadores:"):
            rastreadores = texto.replace("Rastreadores:", "").strip()
            span_tag = elemento.find('span')
            if span_tag:
                rastreadores += " " + span_tag.get_text(strip=True)
            dados_veiculo["rastreadores"].append(rastreadores)
        elif texto.startswith("Bloqueadores:"):
            bloqueadores = texto.replace("Bloqueadores:", "").strip()
            span_tag = elemento.find('span')
            if span_tag:
                bloqueadores += " " + span_tag.get_text(strip=True)
            dados_veiculo["bloqueadores"].append(bloqueadores)
        elif texto.startswith("Última Vistoria:"):
            ultima_vistoria = texto.replace("Última Vistoria:", "").strip()
            dados_veiculo["Última Vistoria"].append(ultima_vistoria)
        elif texto.startswith("Monitoramento:"):
            monitoramento = texto.replace("Monitoramento:", "").strip()
            span_tag = elemento.find('span')
            if span_tag:
                monitoramento = span_tag.get_text(strip=True)
            dados_veiculo["monitoramento"].append(monitoramento)
        elif texto.startswith("Anotações de Controle:"):
            anotacoes_controle = elemento.find('div', class_='well').text.strip()
            dados_veiculo["Anotações de Controle:"].append(anotacoes_controle)
        else:
            label_tag = elemento.find('b')
            if label_tag:
                label = label_tag.get_text(strip=True).replace(":", "")
                valor = label_tag.next_sibling.strip() if label_tag.next_sibling else ""
                if label.lower() in dados_veiculo:
                    dados_veiculo[label.lower()].append(valor)
            
            
    # Criar sessão
    Session = sessionmaker(bind=engine)
    session = Session()
    
    
    # Cria uma instância da classe Veiculos
    veiculo = Veiculos(
        status=status,
        inclusao=inclusao,
        exclusao=exclusao,
        valor_cota=valor_cota,
        integrante=integrante,
        tipo=dados_veiculo["tipo"][0] if len(dados_veiculo["tipo"]) > 0 else None,
        especie=dados_veiculo["espécie"][0] if len(dados_veiculo["espécie"]) > 0 else None,
        composicao=composicao,
        cod_fipe=cod_fipe,
        valor_principal=valor_principal,
        agregado=agregado,
        indice_participacao=indice_participacao,
        placa1=dados_veiculo["placa"][0] if len(dados_veiculo["placa"]) > 0 else None,
        marca1=dados_veiculo["marca"][0] if len(dados_veiculo["marca"]) > 0 else None,
        modelo1=dados_veiculo["modelo"][0] if len(dados_veiculo["modelo"]) > 0 else None,
        ano_fabricacao1=dados_veiculo["ano fabricação"][0] if len(dados_veiculo["ano fabricação"]) > 0 else None,
        ano_modelo1=dados_veiculo["ano modelo"][0] if len(dados_veiculo["ano modelo"]) > 0 else None,
        renavam1=dados_veiculo["renavam"][0] if len(dados_veiculo["renavam"]) > 0 else None,
        chassi1=dados_veiculo["chassi"][0] if len(dados_veiculo["chassi"]) > 0 else None,
        cor1=dados_veiculo["cor"][0] if len(dados_veiculo["cor"]) > 0 else None,
        estado1=dados_veiculo["estado"][0] if len(dados_veiculo["estado"]) > 0 else None,
        cidade1=dados_veiculo["cidade"][0] if len(dados_veiculo["cidade"]) > 0 else None,
        documento1=dados_veiculo["documento"][0] if len(dados_veiculo["documento"]) > 0 else None,
        especie1=dados_veiculo["espécie"][1] if len(dados_veiculo["espécie"]) > 1 else None,
        tipo1=dados_veiculo["tipo"][1] if len(dados_veiculo["tipo"]) > 1 else None,
        carroceria1=dados_veiculo["carroceria"][0] if len(dados_veiculo["carroceria"]) > 0 else None,
        cap_max_carga1=dados_veiculo["Cap. Max. Carga"][0] if len(dados_veiculo["Cap. Max. Carga"]) > 0 else None,
        peso_bruto_total1=dados_veiculo["Peso Bruto Total"][0] if len(dados_veiculo["Peso Bruto Total"]) > 0 else None,
        cap_max_tracao1=dados_veiculo["Cap. Max. Tração"][0] if len(dados_veiculo["Cap. Max. Tração"]) > 0 else None,
        numero_motor1=dados_veiculo["N°. Motor"][0] if len(dados_veiculo["N°. Motor"]) > 0 else None,
        potencia1=dados_veiculo["potência"][0] if len(dados_veiculo["potência"]) > 0 else None,
        lotacao1=dados_veiculo["lotação"][0] if len(dados_veiculo["lotação"]) > 0 else None,
        eixos1=dados_veiculo["eixos"][0] if len(dados_veiculo["eixos"]) > 0 else None,
        numero_crv1=dados_veiculo["Nº. CRV"][0] if len(dados_veiculo["Nº. CRV"]) > 0 else None,
        numero_seg_cla1=dados_veiculo["Nº. Seg. CLA"][0] if len(dados_veiculo["Nº. Seg. CLA"]) > 0 else None,
        observacoes1=dados_veiculo["Observações"][0] if len(dados_veiculo["Observações"]) > 0 else None,
        placa2=dados_veiculo["placa"][1] if len(dados_veiculo["placa"]) > 1 else None,
        marca2=dados_veiculo["marca"][1] if len(dados_veiculo["marca"]) > 1 else None,
        modelo2=dados_veiculo["modelo"][1] if len(dados_veiculo["modelo"]) > 1 else None,
        ano_fabricacao2=dados_veiculo["ano fabricação"][1] if len(dados_veiculo["ano fabricação"]) > 1 else None,
        ano_modelo2=dados_veiculo["ano modelo"][1] if len(dados_veiculo["ano modelo"]) > 1 else None,
        renavam2=dados_veiculo["renavam"][1] if len(dados_veiculo["renavam"]) > 1 else None,
        chassi2=dados_veiculo["chassi"][1] if len(dados_veiculo["chassi"]) > 1 else None,
        cor2=dados_veiculo["cor"][1] if len(dados_veiculo["cor"]) > 1 else None,
        estado2=dados_veiculo["estado"][1] if len(dados_veiculo["estado"]) > 1 else None,
        cidade2=dados_veiculo["cidade"][1] if len(dados_veiculo["cidade"]) > 1 else None,
        documento2=dados_veiculo["documento"][1] if len(dados_veiculo["documento"]) > 1 else None,
        especie2=dados_veiculo["espécie"][2] if len(dados_veiculo["espécie"]) > 2 else None,
        tipo2=dados_veiculo["tipo"][2] if len(dados_veiculo["tipo"]) > 2 else None,
        carroceria2=dados_veiculo["carroceria"][1] if len(dados_veiculo["carroceria"]) > 1 else None,
        cap_max_carga2=dados_veiculo["Cap. Max. Carga"][1] if len(dados_veiculo["Cap. Max. Carga"]) > 1 else None,
        peso_bruto_total2=dados_veiculo["Peso Bruto Total"][1] if len(dados_veiculo["Peso Bruto Total"]) > 1 else None,
        cap_max_tracao2=dados_veiculo["Cap. Max. Tração"][1] if len(dados_veiculo["Cap. Max. Tração"]) > 1 else None,
        numero_motor2=dados_veiculo["N°. Motor"][1] if len(dados_veiculo["N°. Motor"]) > 1 else None,
        potencia2=dados_veiculo["potência"][1] if len(dados_veiculo["potência"]) > 1 else None,
        lotacao2=dados_veiculo["lotação"][1] if len(dados_veiculo["lotação"]) > 1 else None,
        eixos2=dados_veiculo["eixos"][1] if len(dados_veiculo["eixos"]) > 1 else None,
        numero_crv2=dados_veiculo["Nº. CRV"][1] if len(dados_veiculo["Nº. CRV"]) > 1 else None,
        numero_seg_cla2=dados_veiculo["Nº. Seg. CLA"][1] if len(dados_veiculo["Nº. Seg. CLA"]) > 1 else None,
        observacoes2=dados_veiculo["Observações"][1] if len(dados_veiculo["Observações"]) > 1 else None,
        placa3=dados_veiculo["placa"][2] if len(dados_veiculo["placa"]) > 2 else None,
        marca3=dados_veiculo["marca"][2] if len(dados_veiculo["marca"]) > 2 else None,
        modelo3=dados_veiculo["modelo"][2] if len(dados_veiculo["modelo"]) > 2 else None,
        ano_fabricacao3=dados_veiculo["ano fabricação"][2] if len(dados_veiculo["ano fabricação"]) > 2 else None,
        ano_modelo3=dados_veiculo["ano modelo"][2] if len(dados_veiculo["ano modelo"]) > 2 else None,
        renavam3=dados_veiculo["renavam"][2] if len(dados_veiculo["renavam"]) > 2 else None,
        chassi3=dados_veiculo["chassi"][2] if len(dados_veiculo["chassi"]) > 2 else None,
        cor3=dados_veiculo["cor"][2] if len(dados_veiculo["cor"]) > 2 else None,
        estado3=dados_veiculo["estado"][2] if len(dados_veiculo["estado"]) > 2 else None,
        cidade3=dados_veiculo["cidade"][2] if len(dados_veiculo["cidade"]) > 2 else None,
        documento3=dados_veiculo["documento"][2] if len(dados_veiculo["documento"]) > 2 else None,
        especie3=dados_veiculo["espécie"][3] if len(dados_veiculo["espécie"]) > 3 else None,
        tipo3=dados_veiculo["tipo"][3] if len(dados_veiculo["tipo"]) > 3 else None,
        carroceria3=dados_veiculo["carroceria"][2] if len(dados_veiculo["carroceria"]) > 2 else None,
        cap_max_carga3=dados_veiculo["Cap. Max. Carga"][2] if len(dados_veiculo["Cap. Max. Carga"]) > 2 else None,
        peso_bruto_total3=dados_veiculo["Peso Bruto Total"][2] if len(dados_veiculo["Peso Bruto Total"]) > 2 else None,
        cap_max_tracao3=dados_veiculo["Cap. Max. Tração"][2] if len(dados_veiculo["Cap. Max. Tração"]) > 2 else None,
        numero_motor3=dados_veiculo["N°. Motor"][2] if len(dados_veiculo["N°. Motor"]) > 2 else None,
        potencia3=dados_veiculo["potência"][2] if len(dados_veiculo["potência"]) > 2 else None,
        lotacao3=dados_veiculo["lotação"][2] if len(dados_veiculo["lotação"]) > 2 else None,
        eixos3=dados_veiculo["eixos"][2] if len(dados_veiculo["eixos"]) > 2 else None,
        numero_crv3=dados_veiculo["Nº. CRV"][2] if len(dados_veiculo["Nº. CRV"]) > 2 else None,
        numero_seg_cla3=dados_veiculo["Nº. Seg. CLA"][2] if len(dados_veiculo["Nº. Seg. CLA"]) > 2 else None,
        observacoes3=dados_veiculo["Observações"][2] if len(dados_veiculo["Observações"]) > 2 else None,
        rastreadores=dados_veiculo["rastreadores"][0] if dados_veiculo["rastreadores"] else None,
        bloqueadores=dados_veiculo["bloqueadores"][0] if dados_veiculo["bloqueadores"] else None,
        ultima_vistoria=dados_veiculo["Última Vistoria"][0] if dados_veiculo["Última Vistoria"] else None,
        monitoramento=dados_veiculo["monitoramento"][0] if dados_veiculo["monitoramento"] else None,
        anotacoes_controle=dados_veiculo["Anotações de Controle:"][0] if dados_veiculo["Anotações de Controle:"] else None,
        estado_grupo=estado_grupo,
    )

    # Adiciona a instância à sessão e tenta salvar no banco de dados
    try:
        session.add(veiculo)
        session.commit()
    except IntegrityError as e:
        session.rollback()
        print(f"Erro ao inserir no banco de dados: {e}")

    # Fecha a sessão
    session.close()
                

except Exception as e:
    print(f"Erro ao localizar os dados: {e}")

finally:
    # Fecha o navegador
    driver.quit()