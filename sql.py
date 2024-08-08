from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import sessionmaker, relationship

# Configurar a conexão com o banco de dados PostgreSQL
# Substitua 'username', 'password', 'host', 'port' e 'database' pelos detalhes do seu banco de dados PostgreSQL
engine = create_engine('postgresql://postgres:D836MpYz82eL79odbC3ZFa@cargo.trackbrasil.com.br:5432/htx_bk', echo=True)
Base = declarative_base()

# Definir o modelo de classe
class DadosIntegrantes(Base):
    __tablename__ = 'integrantes'
    id = Column(Integer, primary_key=True, autoincrement=True)
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
    logradouro = Column(String)
    numero = Column(String)
    bairro = Column(String)
    cep = Column(String)
    complemento = Column(String)
    referencia = Column(String)
    estado = Column(String)
    cidade = Column(String)
    celular_preferencial = Column(String)
    celular_complementar = Column(String)
    telefone = Column(String)
    email = Column(String)
    vigencia_contrato = Column(String)
    metodo_cobranca = Column(String)
    indice_participacao = Column(String)
    integracao_trackbrasil = Column(String)

    __table_args__ = (
        UniqueConstraint('cnpj', name='uq_cnpj'),  # Define a restrição de unicidade
    )


# Definir o modelo de classe para a tabela 'veiculos'
class VeiculosIntegrantes(Base):
    __tablename__ = 'veiculos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_integrante = Column(Integer, ForeignKey('integrantes.id'))  # Chave estrangeira para a tabela 'integrantes'
    ano_modelo = Column(String)
    status = Column(String)
    inclusao = Column(String)
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
    ano_fabricacao = Column(Integer)
    ano_modelo = Column(Integer)
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