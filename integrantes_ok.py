from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from sqlalchemy.exc import IntegrityError
from sql import engine, DadosClientes, Aportes, Cobrancas_2
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

while True:
    try:
        # Localiza todos os botões "VER" na tabela
        botoes_ver = driver.find_elements(By.CSS_SELECTOR, '#listar_integrantes a.info_cliente')
        print(f"Total de botões 'VER' encontrados: {len(botoes_ver)}")


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
                time.sleep(2)

                # Extrai o HTML da página
                html = driver.page_source

                # Analisa o HTML com BeautifulSoup
                if html:
                    soup = BeautifulSoup(html, 'html.parser')
                else:
                    print("HTML vazio! Verifique a requisição ou o arquivo.")

                status = None
                inclusao = None
                vigencia = None
                exclusao = None

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
                tipo_vigencia_ou_exclusao = soup.find('div', class_='sub_status').find_all('span')[1].text.strip()
                vigencia_ou_exclusao = soup.find('div', class_='sub_status').find_all('span')[1].next_sibling.strip()

                if "Vigência do Contrato" in tipo_vigencia_ou_exclusao:
                    vigencia = vigencia_ou_exclusao
                else:
                    exclusao = vigencia_ou_exclusao

                print(f"Inclusão: {inclusao}")
                print(f"{tipo_vigencia_ou_exclusao}: {vigencia_ou_exclusao}")

                # Localiza o contêiner principal da aba "dados"
                dados_container = soup.find('div', class_='tab dados', style='display:block;')

                if dados_container:
                    # Captura múltiplos elementos de endereço dentro da aba "dados"
                    logradouro_elements = dados_container.find_all('div', class_='six columns fv')

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
                        elif 'Estado:' in label:
                            estados.append(value)
                        elif 'Cidade' in label:
                            cidades.append(value)

                    # Captura os outros campos dentro da aba "dados"
                    elementos = dados_container.find_all('div', class_='six columns fv')
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
                    estado_grupo = 'Grande SC'

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

                else:
                    print("Contêiner 'dados' não encontrado.")
                
                # ========== SALVAR CLIENTE NO BANCO ANTES DE CONTINUAR ==========
                # Criar sessão
                Session = sessionmaker(bind=engine)
                session = Session()

                # Verificar se o cliente já está cadastrado
                cliente_existente = session.query(DadosClientes).filter_by(
                    cl_cnpj=cnpj, 
                    cl_estado_grupo=estado_grupo, 
                    cl_cpf=cpf, 
                    cl_status=status
                ).first()
                
                if cliente_existente:
                    print(f"Cliente com CNPJ {cnpj}, estado Grupo {estado_grupo} e cpf {cpf} e status {status} já está cadastrado. Pulando para o próximo.")
                    session.close()
                    continue
                
                # Processa endereços e salva cliente
                cliente_salvo = False
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

                    novo_dado = DadosClientes(
                        cl_status=status,
                        cl_data_inclusao=inclusao,
                        cl_data_vigencia=vigencia,
                        cl_data_exclusao=exclusao,
                        cl_razao_social=razao_social,
                        cl_cnpj=cnpj,
                        cl_nome=nome,
                        cl_nacionalidade=nacionalidade,
                        cl_estado_civil=estado_civil,
                        cl_profissao=profissao,
                        cl_rg=rg,
                        cl_orgao_exp=orgao_exp,
                        cl_cpf=cpf,
                        cl_nascimento=nascimento,
                        cl_logradouro=logradouro1,
                        cl_numero=numero1,
                        cl_bairro=bairro1,
                        cl_cep=cep1,
                        cl_complemento=complemento1,
                        cl_referencia=referencia1,
                        cl_estado=estado1,
                        cl_cidade=cidade1,
                        cl_adm_logradouro=logradouro2,
                        cl_adm_numero=numero2,
                        cl_adm_bairro=bairro2,
                        cl_adm_cep=cep2,
                        cl_adm_complemento=complemento2,
                        cl_adm_referencia=referencia2,
                        cl_adm_estado=estado2,
                        cl_adm_cidade=cidade2,
                        cl_celular_preferencial=celular_preferencial,
                        cl_celular_complementar=celular_complementar,
                        cl_telefone=telefone,
                        cl_email=email,
                        cl_vigencia_contrato=vigencia_contrato,
                        cl_metodo_cobranca=metodo_cobranca,
                        cl_indice_participacao=indice_participacao,
                        cl_integracao_trackbrasil=integracao_trackbrasil,
                        cl_estado_grupo=estado_grupo
                    )

                    try:
                        # Adicionar e confirmar a transação
                        session.add(novo_dado)
                        session.commit()
                        print(f"✓ Cliente salvo com sucesso! ID: {novo_dado.cl_id}")
                        cliente_salvo = True
                        break  # Só precisa salvar uma vez
                    except IntegrityError as e:
                        if 'uq_cnpj_estado_grupo' in str(e.orig):
                            print(f"Erro: O CNPJ {cnpj}, estado Grupo {estado_grupo} e cpf {cpf} já existem no banco de dados.")
                        else:
                            print(f"Erro de integridade: {e}")
                        session.rollback()
                        session.close()
                        continue  # Pula para próximo cliente
                
                if not cliente_salvo:
                    print("Erro ao salvar cliente. Pulando para o próximo.")
                    session.close()
                    continue
                
                # ========== NAVEGAÇÃO PARA ABA FINANCEIRO ==========
                # Localiza a aba "financeiro" dentro do modal
                aba_financeiro = driver.find_element(By.CSS_SELECTOR, 'li#licobint[data-id="financeiro"]')
                aba_financeiro.click()
                time.sleep(2)
                
                # ========== CAPTURA E SALVA APORTES ==========
                html_financeiro = driver.page_source
                soup_financeiro = BeautifulSoup(html_financeiro, 'html.parser')
                
                aportes_capturados = []
                total_aportes_calculados = None
                caixa_total_valor = None
                
                fundo_rateio_div = soup_financeiro.find('div', id='lfundo')
                if fundo_rateio_div:
                    tabela_fundo = fundo_rateio_div.find('table', class_='table_simples')
                    if tabela_fundo:
                        linhas = tabela_fundo.find('tbody').find_all('tr')
                        
                        print("\n=== FUNDO DE RATEIO ===")
                        for linha in linhas[:-1]:  # Ignora a última linha (totais)
                            colunas = linha.find_all('td')
                            if len(colunas) >= 6:
                                aporte_id = colunas[0].text.strip()
                                data = colunas[1].text.strip()
                                tipo = colunas[2].text.strip()
                                valor = colunas[3].text.strip()
                                valor_pago = colunas[4].text.strip()
                                percentual = colunas[5].text.strip()
                                
                                aportes_capturados.append({
                                    'id': aporte_id,
                                    'data': data,
                                    'tipo': tipo,
                                    'valor': valor,
                                    'valor_pago': valor_pago,
                                    'percentual': percentual
                                })
                                
                                print(f"ID: {aporte_id} | Data: {data} | Tipo: {tipo} | Valor: {valor} | Pago: {valor_pago} | %: {percentual}")
                        
                        # Captura linha de totais
                        linha_total = linhas[-1]
                        colunas_total = linha_total.find_all('td')
                        if len(colunas_total) >= 2:
                            span_total = colunas_total[0].find('span')
                            span_caixa = colunas_total[1].find('span')
                            
                            if span_total:
                                total_aportes_calculados = span_total.text.strip()
                            if span_caixa:
                                caixa_total_valor = span_caixa.text.strip()
                            
                            print(f"\nTotal Aportes: {total_aportes_calculados}")
                            print(f"Caixa Total: {caixa_total_valor}")
                        print("=" * 50 + "\n")
                        
                        # Salva os aportes relacionados ao cliente
                        if aportes_capturados:
                            print(f"Salvando {len(aportes_capturados)} aportes para o cliente {novo_dado.cl_id}...")
                            for aporte_data in aportes_capturados:
                                aporte = Aportes(
                                    ap_cliente_id=novo_dado.cl_id,
                                    ap_id_aporte=aporte_data['id'],
                                    ap_data=aporte_data['data'],
                                    ap_tipo=aporte_data['tipo'],
                                    ap_valor=aporte_data['valor'],
                                    ap_valor_pago=aporte_data['valor_pago'],
                                    ap_percentual=aporte_data['percentual'],
                                    ap_total_aportes_calculados=total_aportes_calculados,
                                    ap_caixa_total=caixa_total_valor
                                )
                                session.add(aporte)
                            session.commit()
                            print(f"✓ Aportes salvos com sucesso! (Total: {total_aportes_calculados}, Caixa: {caixa_total_valor})")
                else:
                    print("Fundo de Rateio não encontrado.")
                
                # ========== CAPTURA RESUMO DE COBRANÇAS ==========
                # Captura dados do resumo de cobranças
                html_financeiro = driver.page_source
                soup_financeiro = BeautifulSoup(html_financeiro, 'html.parser')
                
                print("\n=== RESUMO DE COBRANÇAS ===")
                div_sifint = soup_financeiro.find('div', class_='sifint')
                if div_sifint:
                    # Extrai cada tipo de cobrança
                    tipos_cobranca = div_sifint.find_all('div', class_='lis_cbr')
                    for tipo in tipos_cobranca:
                        nome = tipo.find('span').text.strip()
                        valores = tipo.find('div').get_text(separator='|').split('|')
                        total = valores[1].strip() if len(valores) > 1 else ""
                        pendente = valores[2].strip() if len(valores) > 2 else ""
                        print(f"{nome}: Total {total} | Pendente {pendente}")
                    
                    # Extrai totais gerais
                    sub_status = div_sifint.find('div', class_='sub_status_cbr')
                    if sub_status:
                        totais = sub_status.find_all('div', class_='slis_cbr')
                        for total_div in totais:
                            texto = total_div.get_text(strip=True)
                            print(texto)
                print("=" * 50 + "\n")
                
                # Localiza todos os botões de info de cobranças
                botoes_info_cobranca = driver.find_elements(By.CSS_SELECTOR, 'i.info_cobranca.ici')
                print(f"Total de cobranças encontradas: {len(botoes_info_cobranca)}\n")
                
                # Processa cada modal de cobrança
                cobrancas_detalhadas = []  # Lista para armazenar cobranças
                
                for idx, botao_info in enumerate(botoes_info_cobranca):
                    try:
                        # Rola até o elemento e usa JavaScript para clicar
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", botao_info)
                        time.sleep(0.3)
                        driver.execute_script("arguments[0].click();", botao_info)
                        
                        # Aguarda o modal aparecer
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'div#modal1.modal.fade.in'))
                        )
                        time.sleep(1.5)  # Tempo adicional para carregar conteúdo completo
                        
                        # Garante que estamos na aba "dados"
                        try:
                            aba_dados_btn = driver.find_element(By.CSS_SELECTOR, 'div#modal1 li[data-id="dados"]')
                            if aba_dados_btn:
                                driver.execute_script("arguments[0].click();", aba_dados_btn)
                                time.sleep(0.5)
                        except:
                            pass  # Se não encontrar, provavelmente já está na aba dados
                        
                        # Captura HTML do modal ativo especificamente
                        modal_element = driver.find_element(By.CSS_SELECTOR, 'div#modal1')
                        html_modal = modal_element.get_attribute('outerHTML')
                        soup_modal = BeautifulSoup(html_modal, 'html.parser')
                        
                        # Localiza a aba "dados" dentro do modal-body
                        aba_dados = soup_modal.find('div', class_='tab dados')
                        
                        if aba_dados:
                            print(f"\n=== COBRANÇA {idx + 1} ===")
                            
                            # Extrai tipo de cobrança (título)
                            tipo_cobranca_elem = aba_dados.find('span', class_='font-danger')
                            tipo_cobranca = tipo_cobranca_elem.text.strip() if tipo_cobranca_elem else ""
                            
                            # Extrai integrante
                            integrante_div = aba_dados.find('div', class_='twelve columns fv')
                            integrante = ""
                            if integrante_div:
                                texto_integrante = integrante_div.text.strip()
                                integrante = texto_integrante.replace("Integrante:", "").strip()
                            
                            # Extrai campos das linhas
                            id_cobranca = ""
                            nosso_numero = ""
                            vencimento = ""
                            emissao = ""
                            vencimento_original = ""
                            numero_parcela = ""
                            qtd_parcelas = ""
                            protesto_automatico = ""
                            dias_protestar = ""
                            banco = ""
                            conta = ""
                            remessado = ""
                            status_cobranca = ""
                            
                            # Percorre todas as divs com classe "fv" para extrair os dados
                            campos_fv = aba_dados.find_all('div', class_='fv')
                            for campo in campos_fv:
                                texto = campo.text.strip()
                                
                                if "Id./Nosso Número:" in texto:
                                    # Separa Id e Nosso Número
                                    partes = texto.replace("Id./Nosso Número:", "").strip().split('/')
                                    id_cobranca = partes[0].strip() if len(partes) > 0 else ""
                                    nosso_numero = partes[1].strip() if len(partes) > 1 else ""
                                elif "Vencimento:" in texto and "Original" not in texto:
                                    vencimento = texto.replace("Vencimento:", "").strip()
                                elif "Emissão:" in texto:
                                    emissao = texto.replace("Emissão:", "").strip()
                                elif "Vencimento Original:" in texto:
                                    vencimento_original = texto.replace("Vencimento Original:", "").strip()
                                elif "N° da Parcela:" in texto:
                                    numero_parcela = texto.replace("N° da Parcela:", "").strip()
                                elif "Qtd. de Parcelas:" in texto:
                                    qtd_parcelas = texto.replace("Qtd. de Parcelas:", "").strip()
                                elif "Protesto Automático:" in texto:
                                    protesto_automatico = texto.replace("Protesto Automático:", "").strip()
                                elif "Dias p/ Protestar:" in texto:
                                    dias_protestar = texto.replace("Dias p/ Protestar:", "").strip()
                                elif "Banco:" in texto:
                                    banco = texto.replace("Banco:", "").strip()
                                elif "Conta:" in texto:
                                    conta = texto.replace("Conta:", "").strip()
                                elif "Remessado:" in texto:
                                    remessado = texto.replace("Remessado:", "").strip()
                                elif "Status:" in texto:
                                    # O status pode conter tags span, então pegamos o texto da label
                                    label_status = campo.find('span', class_='label')
                                    status_cobranca = label_status.text.strip() if label_status else ""
                            
                            # Extrai valor principal
                            valor_principal = ""
                            # Busca na coluna da direita (four columns)
                            four_columns = aba_dados.find('div', class_='four columns')
                            if four_columns:
                                h3_valor = four_columns.find('h3', class_='form_section')
                                if h3_valor:
                                    b_tag = h3_valor.find('b')
                                    if b_tag:
                                        valor_principal = b_tag.text.strip()
                            
                            # Extrai taxas bancárias
                            taxas_bancarias = ""
                            if four_columns:
                                well_div = four_columns.find('div', class_='well')
                                if well_div:
                                    taxas_bancarias = well_div.text.strip()
                            
                            # Armazena os dados capturados
                            cobranca_dados = {
                                'tipo_cobranca': tipo_cobranca,
                                'integrante': integrante,
                                'id_cobranca': id_cobranca,
                                'nosso_numero': nosso_numero,
                                'vencimento': vencimento,
                                'emissao': emissao,
                                'vencimento_original': vencimento_original,
                                'numero_parcela': numero_parcela,
                                'qtd_parcelas': qtd_parcelas,
                                'protesto_automatico': protesto_automatico,
                                'dias_protestar': dias_protestar,
                                'banco': banco,
                                'conta': conta,
                                'remessado': remessado,
                                'status': status_cobranca,
                                'valor_principal': valor_principal,
                                'taxas_bancarias': taxas_bancarias
                            }
                            
                            cobrancas_detalhadas.append(cobranca_dados)
                            
                            # Imprime os dados capturados
                            print(f"Tipo: {tipo_cobranca}")
                            print(f"Integrante: {integrante}")
                            print(f"ID/Nosso Número: {id_cobranca} / {nosso_numero}")
                            print(f"Vencimento: {vencimento}")
                            print(f"Emissão: {emissao}")
                            print(f"Vencimento Original: {vencimento_original}")
                            print(f"N° da Parcela: {numero_parcela}")
                            print(f"Qtd. de Parcelas: {qtd_parcelas}")
                            print(f"Protesto Automático: {protesto_automatico}")
                            print(f"Dias p/ Protestar: {dias_protestar}")
                            print(f"Banco: {banco}")
                            print(f"Conta: {conta}")
                            print(f"Remessado: {remessado}")
                            print(f"Status: {status_cobranca}")
                            print(f"Valor: {valor_principal}")
                            print(f"Taxas: {taxas_bancarias}")
                            
                            # Agora clica na aba "historico" para capturar esses dados
                            try:
                                aba_historico_btn = driver.find_element(By.CSS_SELECTOR, 'div#modal1 li[data-id="historico"]')
                                driver.execute_script("arguments[0].click();", aba_historico_btn)
                                time.sleep(1)
                                
                                # Captura HTML atualizado do modal com a aba histórico
                                modal_element_hist = driver.find_element(By.CSS_SELECTOR, 'div#modal1')
                                html_modal_hist = modal_element_hist.get_attribute('outerHTML')
                                soup_modal_hist = BeautifulSoup(html_modal_hist, 'html.parser')
                                
                                # Localiza a aba "historico"
                                aba_historico = soup_modal_hist.find('div', class_='tab historico')
                                
                                if aba_historico:
                                    # Extrai "Última Consulta"
                                    ultima_consulta = ""
                                    ultima_consulta_div = aba_historico.find('div', class_='twelve columns fv')
                                    if ultima_consulta_div:
                                        texto_consulta = ultima_consulta_div.text.strip()
                                        ultima_consulta = texto_consulta.replace("Última Consulta:", "").strip()
                                    
                                    # Extrai histórico de interações da tabela
                                    historico_interacoes = []
                                    tabela_historico = aba_historico.find('table', class_='table_simples')
                                    if tabela_historico:
                                        linhas_hist = tabela_historico.find('tbody').find_all('tr')
                                        for linha in linhas_hist:
                                            colunas_hist = linha.find_all('td')
                                            if len(colunas_hist) >= 4:
                                                tipo_label = colunas_hist[0].find('span')
                                                tipo_interacao = tipo_label.text.strip() if tipo_label else ""
                                                data_interacao = colunas_hist[1].text.strip()
                                                instrucao = colunas_hist[2].text.strip()
                                                motivos = colunas_hist[3].text.strip()
                                                
                                                historico_interacoes.append({
                                                    'tipo': tipo_interacao,
                                                    'data': data_interacao,
                                                    'instrucao': instrucao,
                                                    'motivos': motivos
                                                })
                                    
                                    # Adiciona ao dicionário de cobrança
                                    cobranca_dados['ultima_consulta'] = ultima_consulta
                                    cobranca_dados['historico_interacoes'] = historico_interacoes
                                    
                                    # Imprime dados do histórico
                                    print(f"Última Consulta: {ultima_consulta}")
                                    if historico_interacoes:
                                        print("Histórico de Interações:")
                                        for interacao in historico_interacoes:
                                            print(f"  [{interacao['tipo']}] {interacao['data']} - {interacao['instrucao']} - {interacao['motivos']}")
                                    
                            except Exception as e_hist:
                                print(f"Erro ao capturar histórico: {str(e_hist)}")
                            
                            print("=" * 50)
                            
                        # Fecha o modal usando ESC ou clicando fora
                        try:
                            # Tenta fechar com ESC
                            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                            time.sleep(2)  # Aguarda 2 segundos após fechar o modal
                        except:
                            # Se ESC não funcionar, tenta clicar no overlay
                            try:
                                overlay = driver.find_element(By.CSS_SELECTOR, 'div.modal-backdrop, div.fundo_modal')
                                driver.execute_script("arguments[0].click();", overlay)
                                time.sleep(2)
                            except:
                                pass
                        
                    except Exception as e:
                        print(f"Erro ao processar cobrança {idx + 1}: {str(e)}")
                        # Tenta fechar modal em caso de erro
                        try:
                            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
                            time.sleep(2)  # Aguarda 2 segundos após fechar
                        except:
                            pass
                
                print(f"\nTotal de cobranças processadas: {len(cobrancas_detalhadas)}\n")
                
                # Fecha a sessão do banco de dados
                session.close()
                        
            except Exception as e:
                    print(f"Erro ao processar botão {index + 1}: {e}")
                    try:
                        session.close()
                    except:
                        pass
                    continue

        # fecha modal
        pyautogui.click(x=153, y=656)
        time.sleep(1)

        # Verifica se o botão "Próxima" está habilitado
        botao_proxima = driver.find_element(By.ID, 'listar_integrantes_next')
        if "disabled" in botao_proxima.get_attribute("class"):
            print("Botão 'Próxima' está desabilitado. Fim da navegação.")
            break  # Sai do loop se não houver mais páginas
        
        time.sleep(2)
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
