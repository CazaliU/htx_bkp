from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import sessionmaker

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

# Criar a tabela no banco de dados
Base.metadata.create_all(engine)