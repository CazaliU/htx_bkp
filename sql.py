from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import UniqueConstraint
from dotenv import load_dotenv
import os

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

# Obter a URL do banco de dados a partir das variáveis de ambiente
database_url = os.getenv('DATABASE_URL')

# Configurar a conexão com o banco de dados PostgreSQL
engine = create_engine(database_url, echo=True)
Base = declarative_base()

# Definir o modelo de classe
class DadosIntegrantes(Base):
    __tablename__ = 'integrantes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String)
    inclusao = Column(String)
    vigencia = Column(String)
    exclusao = Column(String)
    razao_social = Column(String)
    cnpj = Column(String, unique=True)  # Adiciona a restrição de unicidade
    nome = Column(String)
    nacionalidade = Column(String)
    estado_civil = Column(String)
    profissao = Column(String)
    rg = Column(String)
    orgao_exp = Column(String)
    cpf = Column(String)
    nascimento = Column(String)
    logradouro1 = Column(String)
    numero1 = Column(String)
    bairro1 = Column(String)
    cep1 = Column(String)
    complemento1 = Column(String)
    referencia1 = Column(String)
    estado1 = Column(String)
    cidade1 = Column(String)
    logradouro2 = Column(String)
    numero2 = Column(String)
    bairro2 = Column(String)
    cep2 = Column(String)
    complemento2 = Column(String)
    referencia2 = Column(String)
    estado2 = Column(String)
    cidade2 = Column(String)
    celular_preferencial = Column(String)
    celular_complementar = Column(String)
    telefone = Column(String)
    email = Column(String)
    vigencia_contrato = Column(String)
    metodo_cobranca = Column(String)
    indice_participacao = Column(String)
    integracao_trackbrasil = Column(String)
    estado_grupo = Column(String)

    __table_args__ = (
        UniqueConstraint('cnpj', 'estado_grupo', 'cpf', name='uq_cnpj_cpf_estado_grupo'),  # Define a restrição de unicidade composta
    )


# Definir o modelo de classe para a tabela 'veiculos'
class Veiculos(Base):
    __tablename__ = 'veiculos'
    ve_id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String)
    inclusao = Column(String)
    exclusao = Column(String)
    valor_cota = Column(String)
    integrante = Column(String)
    tipo = Column(String)
    especie = Column(String)
    composicao = Column(String)
    cod_fipe = Column(String)
    valor_principal = Column(String)
    agregado = Column(String)
    indice_participacao = Column(String)
    placa1 = Column(String)
    marca1 = Column(String)
    modelo1 = Column(String)
    ano_fabricacao1 = Column(String)
    ano_modelo1 = Column(String)
    renavam1 = Column(String)
    chassi1 = Column(String)
    cor1 = Column(String)
    estado1 = Column(String)
    cidade1 = Column(String)
    documento1 = Column(String)
    especie1 = Column(String)
    tipo1 = Column(String)
    carroceria1 = Column(String)
    cap_max_carga1 = Column(String)
    peso_bruto_total1 = Column(String)
    cap_max_tracao1 = Column(String)
    numero_motor1 = Column(String)
    potencia1 = Column(String)
    lotacao1 = Column(String)
    eixos1 = Column(String)
    numero_crv1 = Column(String)
    numero_seg_cla1 = Column(String)
    observacoes1 = Column(String)
    placa2 = Column(String)
    marca2 = Column(String)
    modelo2 = Column(String)
    ano_fabricacao2 = Column(String)
    ano_modelo2 = Column(String)
    renavam2 = Column(String)
    chassi2 = Column(String)
    cor2 = Column(String)
    estado2 = Column(String)
    cidade2 = Column(String)
    documento2 = Column(String)
    especie2 = Column(String)
    tipo2 = Column(String)
    carroceria2 = Column(String)
    cap_max_carga2 = Column(String)
    peso_bruto_total2 = Column(String)
    cap_max_tracao2 = Column(String)
    numero_motor2 = Column(String)
    potencia2 = Column(String)
    lotacao2 = Column(String)
    eixos2 = Column(String)
    numero_crv2 = Column(String)
    numero_seg_cla2 = Column(String)
    observacoes2 = Column(String)
    placa3 = Column(String)
    marca3 = Column(String)
    modelo3 = Column(String)
    ano_fabricacao3 = Column(String)
    ano_modelo3 = Column(String)
    renavam3 = Column(String)
    chassi3 = Column(String)
    cor3 = Column(String)
    estado3 = Column(String)
    cidade3 = Column(String)
    documento3 = Column(String)
    especie3 = Column(String)
    tipo3 = Column(String)
    carroceria3 = Column(String)
    cap_max_carga3 = Column(String)
    peso_bruto_total3 = Column(String)
    cap_max_tracao3 = Column(String)
    numero_motor3 = Column(String)
    potencia3 = Column(String)
    lotacao3 = Column(String)
    eixos3 = Column(String)
    numero_crv3 = Column(String)
    numero_seg_cla3 = Column(String)
    observacoes3 = Column(String)
    rastreadores = Column(String)
    bloqueadores = Column(String)
    ultima_vistoria = Column(String)
    monitoramento = Column(String)
    anotacoes_controle = Column(String)
    estado_grupo = Column(String)
    veiculos_cl_id = Column(Integer)

    __table_args__ = (
        UniqueConstraint('placa1', 'estado_grupo', 'status', name='uq_placa1_estado_grupo_status'),  # Define a restrição de unicidade composta
    )

# Criar as tabelas no banco de dados
Base.metadata.create_all(engine)