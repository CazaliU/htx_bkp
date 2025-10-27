from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from sqlalchemy.orm import sessionmaker, session
from sql import engine, Veiculos, DadosClientes
from selenium.webdriver.common.by import By
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from dotenv import load_dotenv
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime
import pyautogui
import time
import os

load_dotenv()

# Função auxiliar para retornar None se o valor for uma string vazia
def empty_to_none(value):
    return value if value else None

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

driver.get('https://www.hitex.com.br/plataforma/index.php?p=gestor-administrativo&g=0')  # Substitua pela URL real da página

# Aguarde a página carregar
time.sleep(25)  # Pode ser necessário ajustar o tempo

while True:
    try:
        # Localiza todos os botões "VER" na página principal
        botoes_principais = driver.find_elements(By.CSS_SELECTOR, '#listar_integrantes a.info_cliente')
        print(f"Total de botões 'VER' encontrados: {len(botoes_principais)}")
        
        for index_principal, botao_principal in enumerate(botoes_principais):
            try:
                cliente_encontrado = True
                print(f"Acessando botão principal {index_principal + 1} de {len(botoes_principais)}")
                
                # Scroll até o botão principal para garantir que ele esteja visível
                driver.execute_script("arguments[0].scrollIntoView();", botao_principal)
                time.sleep(1)
                
                # Clica no botão principal
                botao_principal.click()
                time.sleep(5)  # Aguarde o modal carregar
                
                # Localiza a aba "veículos" dentro do modal
                aba_veiculos = driver.find_element(By.CSS_SELECTOR, 'li[data-id="veiculos"]')
                aba_veiculos.click()
                time.sleep(2)
                
                # Localiza todos os botões "VER" dentro do modal
                botoes_modal = driver.find_elements(By.CSS_SELECTOR, 'table.table_simples.veiculos a.bold.info_veiculo')
                print(f"Total de botões 'VER' no modal: {len(botoes_modal)}")

                # Verifica se não há botões "VER"
                if len(botoes_modal) == 0:
                    print("Nenhum botão 'VER' encontrado. Tentando mostrar desativados...")
                    
                # Localiza e clica no botão "Mostrar Desativados"
                try:
                    botao_mostrar_desativados = driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-sm.btn-info.vmd')
                    botao_mostrar_desativados.click()
                    time.sleep(2)  # Aguarda os botões desativados aparecerem
                    
                # Tenta localizar novamente os botões "VER"
                    botoes_modal = driver.find_elements(By.CSS_SELECTOR, 'table.table_simples.veiculos a.bold.info_veiculo')
                    print(f"Total de botões 'VER' após mostrar desativados: {len(botoes_modal)}")
                except Exception as e:
                    print(f"Erro ao tentar mostrar botões desativados: {e}")
                    # Fecha o modal e vai para o próximo botão principal
                    pyautogui.click(x=153, y=656)
                    time.sleep(1)
                    continue

                # Itera sobre os botões "VER" dentro do modal
                for index_modal, botao_modal in enumerate(botoes_modal):
                    try:
                        print(f"Acessando botão do modal {index_modal + 1} de {len(botoes_modal)}")
                        
                        # Scroll até o botão do modal para garantir que ele esteja visível
                        driver.execute_script("arguments[0].scrollIntoView();", botao_modal)
                        time.sleep(1)

                        # Clica no botão do modal
                        botao_modal.click()
                        time.sleep(2)  # Aguarde o modal carregar
                        
                        # Extrai o HTML da página
                        html = driver.page_source

                        # Analisa o HTML com BeautifulSoup
                        soup = BeautifulSoup(html, 'html.parser')
                        
                        # Extrai o HTML da aba aberta
                        aba_dados = soup.find('div', class_='tab dados', style='display:block;')

                        status = None
                        inclusao = None
                        exclusao = None
                        valor_cota = None

                        if aba_dados:
                            # Captura o status dentro da aba aberta
                            status_element = aba_dados.find('div', class_='label label-success')
                            if not status_element:
                                status_element = aba_dados.find('div', class_='label label-danger')
                            if not status_element:
                                status_element = aba_dados.find('div', class_='label label-warning')  # Adiciona a busca pelo status com 'label label-warning'

                            if status_element:
                                status = status_element.text.strip()
                            else:
                                status = 'Status não encontrado'

                        # Captura os dados de inclusão e exclusão dentro da aba aberta
                        sub_status_element = aba_dados.find('div', class_='sub_status')
                        if sub_status_element:
                            inclusao_element = sub_status_element.find('span', class_='font-success')
                            exclusao_element = sub_status_element.find('span', class_='font-danger')
                    
                            if inclusao_element and inclusao_element.next_sibling:
                                inclusao = inclusao_element.next_sibling.strip()

                            if exclusao_element and exclusao_element.next_sibling:
                                exclusao = exclusao_element.next_sibling.strip()

                            # Busca pela div que contém "Valor / Cotas:" DENTRO da aba dados
                            portlet_options = aba_dados.find('div', class_='portlet-options')
                            if portlet_options:
                                # Busca todos os spans que podem conter o valor da cota
                                spans_cota = portlet_options.find_all('span', class_=['label label-success', 'label label-danger', 'label label-grey'])
                                
                                # Procura pelo span que não contém 'R$' (que seria o valor da cota)
                                for span in spans_cota:
                                    texto = span.get_text(strip=True)
                                    if not 'R$' in texto and ',' in texto:
                                        valor_cota = texto
                                        break
                                        
                                # Se não encontrou, pega o último span (geralmente é a cota)
                                if not valor_cota and spans_cota:
                                    ultimo_span = spans_cota[-1].get_text(strip=True)
                                    if not 'R$' in ultimo_span:
                                        valor_cota = ultimo_span
                        else:
                            print("Aba dados não encontrada")

                        print(f"Valor da cota encontrado: {valor_cota}")

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
                            "proprietário": [],
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
                        
                        # Verificar se a placa1 já está cadastrada no grupo com o mesmo status
                        placa1_existe = session.query(Veiculos).filter_by(
                            ve_placa1=dados_veiculo["placa"][0],
                            ve_estado_grupo=estado_grupo,
                            ve_status=status
                        ).first()
                        if placa1_existe:
                            # Se a placa já existe com o mesmo status, atualiza ve_valor_principal, ve_agregado e ve_valor_cota (se houverem)
                            updated_fields = []
                            try:
                                if valor_principal:
                                    placa1_existe.ve_valor_principal = empty_to_none(valor_principal)
                                    updated_fields.append('ve_valor_principal')
                                if agregado:
                                    placa1_existe.ve_agregado = empty_to_none(agregado)
                                    updated_fields.append('ve_agregado')
                                if valor_cota:
                                    placa1_existe.ve_valor_cota = empty_to_none(valor_cota)
                                    updated_fields.append('ve_valor_cota')

                                # Sempre atualiza timestamp de atualização quando pelo menos um campo for atualizado
                                if updated_fields:
                                    placa1_existe.ve_atualizado_em = datetime.now().isoformat()
                                    updated_fields.append('ve_atualizado_em')
                                    session.commit()
                                    print(f"Atualizado {', '.join(updated_fields)} do veículo {placa1_existe.ve_placa1} (mesmo status)")
                                else:
                                    print(f"Placa {dados_veiculo['placa'][0]} já cadastrada no grupo {estado_grupo} com o status {status} (nenhum campo para atualizar).")

                            except Exception as e:
                                session.rollback()
                                print(f"Erro ao atualizar campos do veículo {placa1_existe.ve_placa1}: {e}")

                            # Fecha o modal interno e pula a inserção normal
                            pyautogui.click(x=153, y=656)
                            time.sleep(1)
                            continue
                        
                        #pegar razao socail ou nome cpf
                        if integrante:
                            try:
                                Session = sessionmaker(bind=engine)
                                session = Session()

                                # Verifica se o integrante já existe no campo 'cl_razao_social' ou 'cl_nome'
                                cliente = session.query(DadosClientes).filter(
                                    or_(
                                        DadosClientes.cl_razao_social.ilike(f"%{integrante}%"),
                                        DadosClientes.cl_nome.ilike(f"%{integrante}%")
                                    )
                                ).first()

                                if cliente:
                                    print(f"ID do cliente encontrado: {cliente.cl_id}")
                                else:
                                    print(f"Cliente com o nome ou razão social '{integrante}' não encontrado.")
                                    cliente_encontrado = False
                                    # Fecha o modal interno
                                    pyautogui.click(x=153, y=656)
                                    time.sleep(1)
                                    break

                            except Exception as e:
                                print(f"Erro ao buscar cliente: {e}")
                            finally:
                                session.close()
                        
                        # Cria uma instância da classe Veiculos
                        veiculo = Veiculos(
                            veiculos_cl_id=cliente.cl_id if cliente else None,
                            ve_status=empty_to_none(status),
                            ve_inclusao=empty_to_none(inclusao),
                            ve_exclusao=empty_to_none(exclusao),
                            ve_valor_cota=empty_to_none(valor_cota),
                            ve_integrante=empty_to_none(integrante),
                            ve_tipo=empty_to_none(dados_veiculo["tipo"][0] if len(dados_veiculo["tipo"]) > 0 else None),
                            ve_especie=empty_to_none(dados_veiculo["espécie"][0] if len(dados_veiculo["espécie"]) > 0 else None),
                            ve_composicao=empty_to_none(composicao),
                            ve_cod_fipe=empty_to_none(cod_fipe),
                            ve_valor_principal=empty_to_none(valor_principal),
                            ve_agregado=empty_to_none(agregado),
                            ve_indice_participacao=empty_to_none(indice_participacao),
                            ve_placa1=empty_to_none(dados_veiculo["placa"][0] if len(dados_veiculo["placa"]) > 0 else None),
                            ve_marca1=empty_to_none(dados_veiculo["marca"][0] if len(dados_veiculo["marca"]) > 0 else None),
                            ve_modelo1=empty_to_none(dados_veiculo["modelo"][0] if len(dados_veiculo["modelo"]) > 0 else None),
                            ve_ano_fabricacao1=empty_to_none(dados_veiculo["ano fabricação"][0] if len(dados_veiculo["ano fabricação"]) > 0 else None),
                            ve_ano_modelo1=empty_to_none(dados_veiculo["ano modelo"][0] if len(dados_veiculo["ano modelo"]) > 0 else None),
                            ve_renavam1=empty_to_none(dados_veiculo["renavam"][0] if len(dados_veiculo["renavam"]) > 0 else None),
                            ve_chassi1=empty_to_none(dados_veiculo["chassi"][0] if len(dados_veiculo["chassi"]) > 0 else None),
                            ve_cor1=empty_to_none(dados_veiculo["cor"][0] if len(dados_veiculo["cor"]) > 0 else None),
                            ve_estado1=empty_to_none(dados_veiculo["estado"][0] if len(dados_veiculo["estado"]) > 0 else None),
                            ve_cidade1=empty_to_none(dados_veiculo["cidade"][0] if len(dados_veiculo["cidade"]) > 0 else None),
                            ve_proprietario1=empty_to_none(dados_veiculo["proprietário"][0] if len(dados_veiculo["proprietário"]) > 0 else None),
                            ve_documento1=empty_to_none(dados_veiculo["documento"][0] if len(dados_veiculo["documento"]) > 0 else None),
                            ve_especie1=empty_to_none(dados_veiculo["espécie"][1] if len(dados_veiculo["espécie"]) > 1 else None),
                            ve_tipo1=empty_to_none(dados_veiculo["tipo"][1] if len(dados_veiculo["tipo"]) > 1 else None),
                            ve_carroceria1=empty_to_none(dados_veiculo["carroceria"][0] if len(dados_veiculo["carroceria"]) > 0 else None),
                            ve_cap_max_carga1=empty_to_none(dados_veiculo["Cap. Max. Carga"][0] if len(dados_veiculo["Cap. Max. Carga"]) > 0 else None),
                            ve_peso_bruto_total1=empty_to_none(dados_veiculo["Peso Bruto Total"][0] if len(dados_veiculo["Peso Bruto Total"]) > 0 else None),
                            ve_cap_max_tracao1=empty_to_none(dados_veiculo["Cap. Max. Tração"][0] if len(dados_veiculo["Cap. Max. Tração"]) > 0 else None),
                            ve_numero_motor1=empty_to_none(dados_veiculo["N°. Motor"][0] if len(dados_veiculo["N°. Motor"]) > 0 else None),
                            ve_potencia1=empty_to_none(dados_veiculo["potência"][0] if len(dados_veiculo["potência"]) > 0 else None),
                            ve_lotacao1=empty_to_none(dados_veiculo["lotação"][0] if len(dados_veiculo["lotação"]) > 0 else None),
                            ve_eixos1=empty_to_none(dados_veiculo["eixos"][0] if len(dados_veiculo["eixos"]) > 0 else None),
                            ve_numero_crv1=empty_to_none(dados_veiculo["Nº. CRV"][0] if len(dados_veiculo["Nº. CRV"]) > 0 else None),
                            ve_numero_seg_cla1=empty_to_none(dados_veiculo["Nº. Seg. CLA"][0] if len(dados_veiculo["Nº. Seg. CLA"]) > 0 else None),
                            ve_observacoes1=empty_to_none(dados_veiculo["Observações"][0] if len(dados_veiculo["Observações"]) > 0 else None),
                            ve_placa2=empty_to_none(dados_veiculo["placa"][1] if len(dados_veiculo["placa"]) > 1 else None),
                            ve_marca2=empty_to_none(dados_veiculo["marca"][1] if len(dados_veiculo["marca"]) > 1 else None),
                            ve_ano_fabricacao2=empty_to_none(dados_veiculo["ano fabricação"][1] if len(dados_veiculo["ano fabricação"]) > 1 else None),
                            ve_ano_modelo2=empty_to_none(dados_veiculo["ano modelo"][1] if len(dados_veiculo["ano modelo"]) > 1 else None),
                            ve_renavam2=empty_to_none(dados_veiculo["renavam"][1] if len(dados_veiculo["renavam"]) > 1 else None),
                            ve_chassi2=empty_to_none(dados_veiculo["chassi"][1] if len(dados_veiculo["chassi"]) > 1 else None),
                            ve_cor2=empty_to_none(dados_veiculo["cor"][1] if len(dados_veiculo["cor"]) > 1 else None),
                            ve_estado2=empty_to_none(dados_veiculo["estado"][1] if len(dados_veiculo["estado"]) > 1 else None),
                            ve_cidade2=empty_to_none(dados_veiculo["cidade"][1] if len(dados_veiculo["cidade"]) > 1 else None),
                            ve_proprietario2=empty_to_none(dados_veiculo["proprietário"][1] if len(dados_veiculo["proprietário"]) > 1 else None),
                            ve_documento2=empty_to_none(dados_veiculo["documento"][1] if len(dados_veiculo["documento"]) > 1 else None),
                            ve_tipo2=empty_to_none(dados_veiculo["tipo"][2] if len(dados_veiculo["tipo"]) > 2 else None),
                            ve_carroceria2=empty_to_none(dados_veiculo["carroceria"][1] if len(dados_veiculo["carroceria"]) > 1 else None),
                            ve_cap_max_carga2=empty_to_none(dados_veiculo["Cap. Max. Carga"][1] if len(dados_veiculo["Cap. Max. Carga"]) > 1 else None),
                            ve_peso_bruto_total2=empty_to_none(dados_veiculo["Peso Bruto Total"][1] if len(dados_veiculo["Peso Bruto Total"]) > 1 else None),
                            ve_cap_max_tracao2=empty_to_none(dados_veiculo["Cap. Max. Tração"][1] if len(dados_veiculo["Cap. Max. Tração"]) > 1 else None),
                            ve_numero_motor2=empty_to_none(dados_veiculo["N°. Motor"][1] if len(dados_veiculo["N°. Motor"]) > 1 else None),
                            ve_potencia2=empty_to_none(dados_veiculo["potência"][1] if len(dados_veiculo["potência"]) > 1 else None),
                            ve_lotacao2=empty_to_none(dados_veiculo["lotação"][1] if len(dados_veiculo["lotação"]) > 1 else None),
                            ve_eixos2=empty_to_none(dados_veiculo["eixos"][1] if len(dados_veiculo["eixos"]) > 1 else None),
                            ve_numero_crv2=empty_to_none(dados_veiculo["Nº. CRV"][1] if len(dados_veiculo["Nº. CRV"]) > 1 else None),
                            ve_numero_seg_cla2=empty_to_none(dados_veiculo["Nº. Seg. CLA"][1] if len(dados_veiculo["Nº. Seg. CLA"]) > 1 else None),
                            ve_observacoes2=empty_to_none(dados_veiculo["Observações"][1] if len(dados_veiculo["Observações"]) > 1 else None),
                            ve_placa3=empty_to_none(dados_veiculo["placa"][2] if len(dados_veiculo["placa"]) > 2 else None),
                            ve_marca3=empty_to_none(dados_veiculo["marca"][2] if len(dados_veiculo["marca"]) > 2 else None),
                            ve_modelo3=empty_to_none(dados_veiculo["modelo"][2] if len(dados_veiculo["modelo"]) > 2 else None),
                            ve_ano_fabricacao3=empty_to_none(dados_veiculo["ano fabricação"][2] if len(dados_veiculo["ano fabricação"]) > 2 else None),
                            ve_ano_modelo3=empty_to_none(dados_veiculo["ano modelo"][2] if len(dados_veiculo["ano modelo"]) > 2 else None),
                            ve_renavam3=empty_to_none(dados_veiculo["renavam"][2] if len(dados_veiculo["renavam"]) > 2 else None),
                            ve_chassi3=empty_to_none(dados_veiculo["chassi"][2] if len(dados_veiculo["chassi"]) > 2 else None),
                            ve_cor3=empty_to_none(dados_veiculo["cor"][2] if len(dados_veiculo["cor"]) > 2 else None),
                            ve_estado3=empty_to_none(dados_veiculo["estado"][2] if len(dados_veiculo["estado"]) > 2 else None),
                            ve_cidade3=empty_to_none(dados_veiculo["cidade"][2] if len(dados_veiculo["cidade"]) > 2 else None),
                            ve_proprietario3=empty_to_none(dados_veiculo["proprietário"][2] if len(dados_veiculo["proprietário"]) > 2 else None),
                            ve_documento3=empty_to_none(dados_veiculo["documento"][2] if len(dados_veiculo["documento"]) > 2 else None),
                            ve_especie3=empty_to_none(dados_veiculo["espécie"][3] if len(dados_veiculo["espécie"]) > 3 else None),
                            ve_tipo3=empty_to_none(dados_veiculo["tipo"][3] if len(dados_veiculo["tipo"]) > 3 else None),
                            ve_carroceria3=empty_to_none(dados_veiculo["carroceria"][2] if len(dados_veiculo["carroceria"]) > 2 else None),
                            ve_cap_max_carga3=empty_to_none(dados_veiculo["Cap. Max. Carga"][2] if len(dados_veiculo["Cap. Max. Carga"]) > 2 else None),
                            ve_peso_bruto_total3=empty_to_none(dados_veiculo["Peso Bruto Total"][2] if len(dados_veiculo["Peso Bruto Total"]) > 2 else None),
                            ve_cap_max_tracao3=empty_to_none(dados_veiculo["Cap. Max. Tração"][2] if len(dados_veiculo["Cap. Max. Tração"]) > 2 else None),
                            ve_numero_motor3=empty_to_none(dados_veiculo["N°. Motor"][2] if len(dados_veiculo["N°. Motor"]) > 2 else None),
                            ve_potencia3=empty_to_none(dados_veiculo["potência"][2] if len(dados_veiculo["potência"]) > 2 else None),
                            ve_lotacao3=empty_to_none(dados_veiculo["lotação"][2] if len(dados_veiculo["lotação"]) > 2 else None),
                            ve_eixos3=empty_to_none(dados_veiculo["eixos"][2] if len(dados_veiculo["eixos"]) > 2 else None),
                            ve_numero_crv3=empty_to_none(dados_veiculo["Nº. CRV"][2] if len(dados_veiculo["Nº. CRV"]) > 2 else None),
                            ve_numero_seg_cla3=empty_to_none(dados_veiculo["Nº. Seg. CLA"][2] if len(dados_veiculo["Nº. Seg. CLA"]) > 2 else None),
                            ve_observacoes3=empty_to_none(dados_veiculo["Observações"][2] if len(dados_veiculo["Observações"]) > 2 else None),
                            ve_rastreadores=empty_to_none(dados_veiculo["rastreadores"][0] if dados_veiculo["rastreadores"] else None),
                            ve_bloqueadores=empty_to_none(dados_veiculo["bloqueadores"][0] if dados_veiculo["bloqueadores"] else None),
                            ve_ultima_vistoria=empty_to_none(dados_veiculo["Última Vistoria"][0] if dados_veiculo["Última Vistoria"] else None),
                            ve_monitoramento=empty_to_none(dados_veiculo["monitoramento"][0] if dados_veiculo["monitoramento"] else None),
                            ve_anotacoes_controle=empty_to_none(dados_veiculo["Anotações de Controle:"][0] if dados_veiculo["Anotações de Controle:"] else None),
                            ve_estado_grupo=empty_to_none(estado_grupo)
                        )

                        # Adiciona a instância à sessão e tenta salvar no banco de dados
                        try:
                            session.add(veiculo)
                            session.commit()
                            print(f"Veículo {dados_veiculo['placa'][0]} inserido com sucesso.")
                        except IntegrityError as e:
                            if 'uq_placa1_estado_grupo_1' in str(e):
                                print(f"Placa {dados_veiculo['placa'][0]} já está cadastrada no grupo {estado_grupo} com o status {status}.")
                            else:
                                print(f"Erro ao inserir o veículo: {e}")
                            session.rollback()
                            
                        # Fecha o modal interno
                        pyautogui.click(x=153, y=656)
                        time.sleep(1)
                            
                    except Exception as e:
                        print(f"Erro ao processar botão do modal {index_modal + 1}: {e}")
                        # Fecha o modal interno
                        pyautogui.click(x=153, y=656)
                        time.sleep(1)
                        continue
                
                # Verifica se o cliente foi encontrado
                if not cliente_encontrado:
                    print("Nenhum cliente encontrado. Indo para o próximo botão principal.")
                    pyautogui.click(x=153, y=656)
                    time.sleep(1)
                    continue  # Vai para o próximo botão principal
                    
                # Fecha o modal principal
                pyautogui.click(x=153, y=656)
                time.sleep(1)
                    
            except Exception as e:
                print(f"Erro ao processar botão principal {index_principal + 1}: {e}")
                continue
        
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

    
