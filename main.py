from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from sqlalchemy.exc import IntegrityError
from sql import engine, DadosIntegrantes
from sqlalchemy.orm import sessionmaker
from selenium import webdriver
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import pyautogui
import time
import os

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Obter as credenciais a partir das variáveis de ambiente
username = os.getenv('APP_USERNAME')
password = os.getenv('APP_PASSWORD')

# BOTAO VER INICIAL
x1, y1 = 46, 540

# NUMERO DE INTEGRANTES
num_insertes = 5000

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
time.sleep(15)  

j = 0
for i in range(0, num_insertes + 1):
    
    # verifica se a iteração é divisivel por 10
    if j == 10:
        pyautogui.click(1835, 957)
        time.sleep(3)
        x1, y1 = 46, 540
        j=0
        
        if i > 63:
            break
        
    # CLICA NO VER
    pyautogui.click(x1, y1)

    time.sleep(3)

    # Espera até que o modal esteja visível
    modal_selector = 'modal-body'  # Substitua pelo seletor que corresponde ao modal
    driver.implicitly_wait(10)  # Espera implícita para o modal

    # Extrai o HTML da página
    html = driver.page_source

    # Analisa o HTML com BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    status = None
    inclusao = None
    vigencia = None

    # Tentar encontrar o elemento com a classe 'label label-success'
    status_element = soup.find('div', class_='label label-success')

    if status_element is not None:
        status = status_element.text.strip()
    else:
        # Se não encontrar 'label label-success', tentar encontrar 'label label-danger'
        status_element = soup.find('div', class_='label label-danger')
        if status_element is not None:
            status = status_element.text.strip()
        else:
            # Tratar a situação quando nenhum dos elementos é encontrado
            status = "Status não encontrado" 

    inclusao = soup.find('div', class_='sub_status').find_all('span')[0].next_sibling.strip()
    vigencia = soup.find('div', class_='sub_status').find_all('span')[1].next_sibling.strip()

    # Captura múltiplos elementos de endereço
    logradouro_elements = soup.find_all('div', class_='six columns fv')

    # Inicializa variáveis para armazenar os valores
    logradouros = []
    numeros = []
    bairros = []
    ceps = []
    complementos = []
    referencias = []
    estados = []
    cidades = []

    # Itera sobre os elementos e armazena os valores nas listas
    for element in logradouro_elements:
        label = element.find('b').get_text(strip=True)
        value = element.get_text(strip=True).replace(label, '').strip()
        
        if 'Logradouro' in label:
            logradouros.append(value)
        elif 'Número' in label:
            numeros.append(value)
        elif 'Bairro' in label:
            bairros.append(value)
        elif 'CEP' in label:
            ceps.append(value)
        elif 'Complemento' in label:
            complementos.append(value)
        elif 'Referência' in label:
            referencias.append(value)
        elif 'Estado' in label:
            estados.append(value)
        elif 'Cidade' in label:
            cidades.append(value)

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
    celular_preferencial = None
    celular_complementar = None
    telefone = None
    email = None
    vigencia_contrato = None
    metodo_cobranca = None
    indice_participacao = None
    integracao_trackbrasil = None
    
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

    # Criar sessão
    Session = sessionmaker(bind=engine)
    session = Session()

    # Itera sobre os valores capturados e insere no banco de dados
    for i in range(0, len(logradouros), 2):
        logradouro1 = logradouros[i] if i < len(logradouros) else None
        numero1 = numeros[i] if i < len(numeros) else None
        bairro1 = bairros[i] if i < len(bairros) else None
        cep1 = ceps[i] if i < len(ceps) else None
        complemento1 = complementos[i] if i < len(complementos) else None
        referencia1 = referencias[i] if i < len(referencias) else None
        estado1 = estados[i] if i < len(estados) else None
        cidade1 = cidades[i] if i < len(cidades) else None

        logradouro2 = logradouros[i+1] if i+1 < len(logradouros) else None
        numero2 = numeros[i+1] if i+1 < len(numeros) else None
        bairro2 = bairros[i+1] if i+1 < len(bairros) else None
        cep2 = ceps[i+1] if i+1 < len(ceps) else None
        complemento2 = complementos[i+1] if i+1 < len(complementos) else None
        referencia2 = referencias[i+1] if i+1 < len(referencias) else None
        estado2 = estados[i+1] if i+1 < len(estados) else None
        cidade2 = cidades[i+1] if i+1 < len(cidades) else None

        novo_dado = DadosIntegrantes(
            status=status,
            inclusao=inclusao,
            vigencia=vigencia,
            razao_social=razao_social,
            cnpj=cnpj,
            nome=nome,
            nacionalidade=nacionalidade,
            estado_civil=estado_civil,
            profissao=profissao,
            rg=rg,
            orgao_exp=orgao_exp,
            cpf=cpf,
            nascimento=nascimento,
            logradouro1=logradouro1,
            numero1=numero1,
            bairro1=bairro1,
            cep1=cep1,
            complemento1=complemento1,
            referencia1=referencia1,
            estado1=estado1,
            cidade1=cidade1,
            logradouro2=logradouro2,
            numero2=numero2,
            bairro2=bairro2,
            cep2=cep2,
            complemento2=complemento2,
            referencia2=referencia2,
            estado2=estado2,
            cidade2=cidade2,
            celular_preferencial=celular_preferencial,
            celular_complementar=celular_complementar,
            telefone=telefone,
            email=email,
            vigencia_contrato=vigencia_contrato,
            metodo_cobranca=metodo_cobranca,
            indice_participacao=indice_participacao,
            integracao_trackbrasil=integracao_trackbrasil
        )

        try: 
            # Adicionar e confirmar a transação
            session.add(novo_dado)
            session.commit()
        except IntegrityError as e:
            if 'uq_cnpj' in str(e.orig):
                print(f"Erro: O CNPJ {novo_dado.cnpj} já existe no banco de dados.")
            else:
                print(f"Erro de integridade: {e}")
            session.rollback()

    time.sleep(4)
    
    # FECHA
    pyautogui.click(1813, 193)
    
    time.sleep(3)
    
    j += 1
    y1 = y1 + 41