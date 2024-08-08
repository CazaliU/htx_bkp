from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from sqlalchemy.exc import IntegrityError
from sql import engine, VeiculosIntegrantes, DadosIntegrantes
from sqlalchemy.orm import sessionmaker, session
from selenium import webdriver
from bs4 import BeautifulSoup
import pyautogui
import time
import os



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

username_input.send_keys('grconsulta')  # Substitua pelo seu nome de usuário
password_input.send_keys('Grupo.Track2024')  # Substitua pela sua senha
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

    # status_element = soup.find('div', class_='label label-sucess')
    
    # if status_element is not None:
    #     status = status_element.text.strip()
    # else:
    #     status_element = soup.find('div', class_='label label-danger')
    #     if status_element is not None:
    #         status = status_element.text.strip()
    #     else:
    #         status = 'Status não encontrado'


    # Captura os dados de status, inclusão e vigência do contrato
    inclusao = soup.find('div', class_='sub_status').find_all('span')[0].next_sibling.strip()
    exclusao = soup.find('div', class_='sub_status').find_all('span')[1].next_sibling.strip()
    
    
    ul_element = soup.find('ul', class_='lateral-tabs')
    ano_modelo = None
    # Iterar sobre os elementos <li> dentro da <ul>
    for li in ul_element.find_all('li'):
        ano_modelo_atual = li.get('ano_modelo')
        if ano_modelo_atual:
            ano_modelo = ano_modelo_atual

    
    
    print(f"Ano Modelo: {ano_modelo}")
    print(f"Status: {status}")
    print(f"Inclusão: {inclusao}")


    elementos = soup.find_all('div', class_=['twelve columns fv', 'six columns fv', 'four columns fv', 'four columns fv input-button'])
    integrante = None
    tipo = None
    especie = None
    composicao = None
    cod_fipe = None
    valor_principal = None
    agregado = None
    indice_participacao = None
    valores_referencia = None
    marca = None
    modelo = None
    placa = None
    ano_fabricacao = None
    ano_modelo = None
    renavam = None
    chassi = None
    cor = None
    estado = None
    cidade = None
    proprietario = None
    documento = None
    carroceria = None
    cap_max_carga = None
    peso_bruto_total = None
    cap_max_tracao = None
    num_motor = None
    potencia = None
    lotacao = None
    eixos = None
    num_crv = None
    num_seg_cla = None
    rastreadores = None
    bloqueadores = None
    ultima_vistoria = None
    monitoramento = None
    
    # Session = sessionmaker(bind=engine)
    # Session = Session()
    

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
        elif texto.startswith("Marca:"):
            marca = texto.replace("Marca:", "").strip()
        elif texto.startswith("Modelo:"):
            modelo = texto.replace("Modelo:", "").strip()
        elif texto.startswith("Placa:"):
            placa = texto.replace("Placa:", "").strip()
        elif texto.startswith("Ano Fabricação:"):
            ano_fabricacao = texto.replace("Ano Fabricação:", "").strip()
        elif texto.startswith("Ano Modelo:"):
            ano_modelo = texto.replace("Ano Modelo:", "").strip()
        elif texto.startswith("Renavam:"):
            renavam = texto.replace("Renavam:", "").strip()
        elif texto.startswith("Chassi:"):
            chassi = texto.replace("Chassi:", "").strip()
        elif texto.startswith("Cor:"):
            cor = texto.replace("Cor:", "").strip()
        elif texto.startswith("Estado:"):
            estado = texto.replace("Estado:", "").strip()
        elif texto.startswith("Cidade:"):
            cidade = texto.replace("Cidade:", "").strip()
        elif texto.startswith("Proprietário:"):
            proprietario = texto.replace("Proprietário:", "").strip()
        elif texto.startswith("Documento:"):
            documento = texto.replace("Documento:", "").strip()
        elif texto.startswith("Carroceria:"):
            carroceria = texto.replace("Carroceria:", "").strip()
        elif texto.startswith("Cap. Max. Carga:"):
            cap_max_carga = texto.replace("Cap. Max. Carga:", "").strip()
        elif texto.startswith("Peso Bruto Total:"):
            peso_bruto_total = texto.replace("Peso Bruto Total:", "").strip()
        elif texto.startswith("Cap. Max. Tração:"):
            cap_max_tracao = texto.replace("Cap. Max. Tração:", "").strip()
        elif texto.startswith("N°. Motor:"):
            num_motor = texto.replace("N°. Motor:", "").strip()
        elif texto.startswith("Potência:"):
            potencia = texto.replace("Potência:", "").strip()
        elif texto.startswith("Lotação:"):
            lotacao = texto.replace("Lotação:", "").strip()
        elif texto.startswith("Eixos:"):
            eixos = texto.replace("Eixos:", "").strip()
        elif texto.startswith("Nº. CRV:"):
            num_crv = texto.replace("Nº. CRV:", "").strip()
        elif texto.startswith("Nº. Seg. CLA:"):
            num_seg_cla = texto.replace("Nº. Seg. CLA:", "").strip()
        elif texto.startswith("Rastreadores:"):
            rastreadores = texto.replace("Rastreadores:", "").strip()
        elif texto.startswith("Bloqueadores:"):
            bloqueadores = texto.replace("Bloqueadores:", "").strip()
        elif texto.startswith("Última Vistoria:"):
            ultima_vistoria = texto.replace("Última Vistoria:", "").strip()
        elif texto.startswith("Monitoramento:"):
            monitoramento = texto.replace("Monitoramento:", "").strip()

    print(f"Integrante: {integrante}")
    print(f"Tipo: {tipo}")
    print(f"Espécie: {especie}")
    print(f"Composição: {composicao}")
    print(f"Cod. Fipe: {cod_fipe}")
    print(f"Valor Principal: {valor_principal}")
    print(f"Agregado: {agregado}")
    print(f"Índice de Participação: {indice_participacao}")
    print(f"Valores de Referência: {valores_referencia}")
    print(f"Marca: {marca}")
    print(f"Modelo: {modelo}")
    print(f"Placa: {placa}")
    print(f"Ano Fabricação: {ano_fabricacao}")
    print(f"Ano Modelo: {ano_modelo}")
    print(f"Renavam: {renavam}")
    print(f"Chassi: {chassi}")
    print(f"Cor: {cor}")
    print(f"Estado: {estado}")
    print(f"Cidade: {cidade}")
    print(f"Proprietário: {proprietario}")
    print(f"Documento: {documento}")
    print(f"Carroceria: {carroceria}")
    print(f"Cap. Max. Carga: {cap_max_carga}")
    print(f"Peso Bruto Total: {peso_bruto_total}")
    print(f"Cap. Max. Tração: {cap_max_tracao}")
    print(f"N°. Motor: {num_motor}")
    print(f"Potência: {potencia}")
    print(f"Lotação: {lotacao}")
    print(f"Eixos: {eixos}")
    print(f"Nº. CRV: {num_crv}")
    print(f"Nº. Seg. CLA: {num_seg_cla}")
    print(f"Rastreadores: {rastreadores}")
    print(f"Bloqueadores: {bloqueadores}")
    print(f"Última Vistoria: {ultima_vistoria}")
    print(f"Monitoramento: {monitoramento}")

    # integrante_obj = session.query(DadosIntegrantes).filter_by(razao_social=integrante).first()
    
    # if not integrante_obj:
    #     id_integrante = integrante_obj.id
    #     print(f"ID do integrante: {id_integrante}")
    # else:
    #     id_integrante = None
    #     print(f"Integrante com razão social '{integrante}' não encontrado no banco de dados.")


    # novo_dado = VeiculosIntegrantes(
    #     id_integrante=id_integrante, 
    #     status=status,
    #     inclusao=inclusao,
    #     exclusao=exclusao,
    #     tipo=tipo,
    #     especie=especie,
    #     composicao =  composicao,
    #     cod_fipe = cod_fipe,
    #     valor_principal = valor_principal,
    #     agregado = agregado,
    #     indice_participacao = indice_participacao,
    #     valores_referencia = valores_referencia,
    #     marca = marca,
    #     modelo = modelo,
    #     placa = placa,
    #     ano_fabricacao = ano_fabricacao,
    #     ano_modelo = ano_modelo,
    #     renavam = renavam,
    #     chassi = chassi,
    #     cor = cor,
    #     estado = estado,
    #     cidade = cidade,
    #     proprietario = proprietario,
    #     documento = documento,
    #     carroceria = carroceria,
    #     cap_max_carga = cap_max_carga,
    #     peso_bruto_total = peso_bruto_total,
    #     cap_max_tracao = cap_max_tracao,
    #     num_motor = num_motor,
    #     potencia = potencia,
    #     lotacao = lotacao,
    #     eixos = eixos,
    #     num_crv = num_crv,
    #     num_seg_cla = num_seg_cla,
    #     rastreadores = rastreadores,
    #     bloqueadores = bloqueadores,
    #     ultima_vistoria = ultima_vistoria,
    #     monitoramento = monitoramento
    # )



except Exception as e:
    print(f"Erro ao localizar os dados: {e}")

finally:
    # Fecha o navegador
    driver.quit()