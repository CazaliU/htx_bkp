from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
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
class VeiculosIntegrantes(Base):
    __tablename__ = 'veiculos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_integrante = Column(Integer, ForeignKey('integrantes.id'))  # Chave estrangeira para a tabela 'integrantes'
    status = Column(String)
    inclusao = Column(String)
    exclusao = Column(String)
    tipo = Column(String)
    especie = Column(String)
    composicao = Column(String)
    cod_fipe = Column(String)
    valor_principal = Column(String)
    agregado = Column(String)
    indice_participacao = Column(String)
    valores_referencia = Column(String)
    marca = Column(String)
    modelo = Column(String)
    placa = Column(String)
    ano_fabricacao = Column(String)
    ano_modelo = Column(String)
    renavam = Column(String)
    chassi = Column(String)
    cor = Column(String)
    estado = Column(String)
    cidade = Column(String)
    proprietario = Column(String)
    documento = Column(String)
    carroceria = Column(String)
    cap_max_carga = Column(String)
    peso_bruto_total = Column(String)
    cap_max_tracao = Column(String)
    num_motor = Column(String)
    potencia = Column(String)
    lotacao = Column(String)
    eixos = Column(String)
    num_crv = Column(String)
    num_seg_cla = Column(String)
    rastreadores = Column(String)
    bloqueadores = Column(String)
    ultima_vistoria = Column(String)
    monitoramento = Column(String)

    # Relacionamento com a tabela 'integrantes'
    integrante = relationship("DadosIntegrantes", back_populates="veiculos")

# Adicionar o relacionamento inverso na classe 'DadosIntegrantes'
DadosIntegrantes.veiculos = relationship("VeiculosIntegrantes", order_by=VeiculosIntegrantes.id, back_populates="integrante")

# Criar as tabelas no banco de dados
Base.metadata.create_all(engine)