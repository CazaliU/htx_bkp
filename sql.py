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
# class DadosIntegrantes(Base):
#     __tablename__ = 'integrantes'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     status = Column(String)
#     inclusao = Column(String)
#     vigencia = Column(String)
#     exclusao = Column(String)
#     razao_social = Column(String)
#     cnpj = Column(String, unique=True)  # Adiciona a restrição de unicidade
#     nome = Column(String)
#     nacionalidade = Column(String)
#     estado_civil = Column(String)
#     profissao = Column(String)
#     rg = Column(String)
#     orgao_exp = Column(String)
#     cpf = Column(String)
#     nascimento = Column(String)
#     logradouro1 = Column(String)
#     numero1 = Column(String)
#     bairro1 = Column(String)
#     cep1 = Column(String)
#     complemento1 = Column(String)
#     referencia1 = Column(String)
#     estado1 = Column(String)
#     cidade1 = Column(String)
#     logradouro2 = Column(String)
#     numero2 = Column(String)
#     bairro2 = Column(String)
#     cep2 = Column(String)
#     complemento2 = Column(String)
#     referencia2 = Column(String)
#     estado2 = Column(String)
#     cidade2 = Column(String)
#     celular_preferencial = Column(String)
#     celular_complementar = Column(String)
#     telefone = Column(String)
#     email = Column(String)
#     vigencia_contrato = Column(String)
#     metodo_cobranca = Column(String)
#     indice_participacao = Column(String)
#     integracao_trackbrasil = Column(String)
#     estado_grupo = Column(String)

#     __table_args__ = (
#         UniqueConstraint('cnpj', 'estado_grupo', 'cpf', name='uq_cnpj_cpf_estado_grupo'),  # Define a restrição de unicidade composta
#     )


# Definir o modelo de classe para a tabela 'veiculos'
class Veiculos(Base):
    __tablename__ = 'veiculos'

    ve_id = Column(Integer, primary_key=True, autoincrement=True)  # ID único para cada veículo
    ve_status = Column(String, nullable=True)
    ve_inclusao = Column(String, nullable=True)
    ve_exclusao = Column(String, nullable=True)
    ve_valor_cota = Column(String, nullable=True)
    ve_integrante = Column(String, nullable=True)
    ve_tipo = Column(String, nullable=True)
    ve_especie = Column(String, nullable=True)
    ve_composicao = Column(String, nullable=True)
    ve_cod_fipe = Column(String, nullable=True)
    ve_valor_principal = Column(String, nullable=True)
    ve_agregado = Column(String, nullable=True)
    ve_indice_participacao = Column(String, nullable=True)
    ve_placa1 = Column(String, nullable=True)
    ve_marca1 = Column(String, nullable=True)
    ve_modelo1 = Column(String, nullable=True)
    ve_ano_fabricacao1 = Column(String, nullable=True)
    ve_ano_modelo1 = Column(String, nullable=True)
    ve_renavam1 = Column(String, nullable=True)
    ve_chassi1 = Column(String, nullable=True)
    ve_cor1 = Column(String, nullable=True)
    ve_estado1 = Column(String, nullable=True)
    ve_cidade1 = Column(String, nullable=True)
    ve_proprietario1 = Column(String, nullable=True)
    ve_documento1 = Column(String, nullable=True)
    ve_especie1 = Column(String, nullable=True)
    ve_tipo1 = Column(String, nullable=True)
    ve_carroceria1 = Column(String, nullable=True)
    ve_cap_max_carga1 = Column(String, nullable=True)
    ve_peso_bruto_total1 = Column(String, nullable=True)
    ve_cap_max_tracao1 = Column(String, nullable=True)
    ve_numero_motor1 = Column(String, nullable=True)
    ve_potencia1 = Column(String, nullable=True)
    ve_lotacao1 = Column(String, nullable=True)
    ve_eixos1 = Column(String, nullable=True)
    ve_numero_crv1 = Column(String, nullable=True)
    ve_numero_seg_cla1 = Column(String, nullable=True)
    ve_observacoes1 = Column(String, nullable=True)
    ve_placa2 = Column(String, nullable=True)
    ve_marca2 = Column(String, nullable=True)
    ve_modelo2 = Column(String, nullable=True)
    ve_ano_fabricacao2 = Column(String, nullable=True)
    ve_ano_modelo2 = Column(String, nullable=True)
    ve_renavam2 = Column(String, nullable=True)
    ve_chassi2 = Column(String, nullable=True)
    ve_cor2 = Column(String, nullable=True)
    ve_estado2 = Column(String, nullable=True)
    ve_cidade2 = Column(String, nullable=True)
    ve_proprietario2 = Column(String, nullable=True)
    ve_documento2 = Column(String, nullable=True)
    ve_especie2 = Column(String, nullable=True)
    ve_tipo2 = Column(String, nullable=True)
    ve_carroceria2 = Column(String, nullable=True)
    ve_cap_max_carga2 = Column(String, nullable=True)
    ve_peso_bruto_total2 = Column(String, nullable=True)
    ve_cap_max_tracao2 = Column(String, nullable=True)
    ve_numero_motor2 = Column(String, nullable=True)
    ve_potencia2 = Column(String, nullable=True)
    ve_lotacao2 = Column(String, nullable=True)
    ve_eixos2 = Column(String, nullable=True)
    ve_numero_crv2 = Column(String, nullable=True)
    ve_numero_seg_cla2 = Column(String, nullable=True)
    ve_observacoes2 = Column(String, nullable=True)
    ve_placa3 = Column(String, nullable=True)
    ve_marca3 = Column(String, nullable=True)
    ve_modelo3 = Column(String, nullable=True)
    ve_ano_fabricacao3 = Column(String, nullable=True)
    ve_ano_modelo3 = Column(String, nullable=True)
    ve_renavam3 = Column(String, nullable=True)
    ve_chassi3 = Column(String, nullable=True)
    ve_cor3 = Column(String, nullable=True)
    ve_estado3 = Column(String, nullable=True)
    ve_cidade3 = Column(String, nullable=True)
    ve_proprietario3 = Column(String, nullable=True)
    ve_documento3 = Column(String, nullable=True)
    ve_especie3 = Column(String, nullable=True)
    ve_tipo3 = Column(String, nullable=True)
    ve_carroceria3 = Column(String, nullable=True)
    ve_cap_max_carga3 = Column(String, nullable=True)
    ve_peso_bruto_total3 = Column(String, nullable=True)
    ve_cap_max_tracao3 = Column(String, nullable=True)
    ve_numero_motor3 = Column(String, nullable=True)
    ve_potencia3 = Column(String, nullable=True)
    ve_lotacao3 = Column(String, nullable=True)
    ve_eixos3 = Column(String, nullable=True)
    ve_numero_crv3 = Column(String, nullable=True)
    ve_numero_seg_cla3 = Column(String, nullable=True)
    ve_observacoes3 = Column(String, nullable=True)
    ve_rastreadores = Column(String, nullable=True)
    ve_bloqueadores = Column(String, nullable=True)
    ve_ultima_vistoria = Column(String, nullable=True)
    ve_monitoramento = Column(String, nullable=True)
    ve_anotacoes_controle = Column(String, nullable=True)
    ve_estado_grupo = Column(String, nullable=True)
    criado_em = Column(String, default="now()", nullable=True)  # Data de criação do registro
    veiculos_cl_id = Column(Integer, ForeignKey('clientes.cl_id', ondelete='SET NULL'), nullable=True)  # Chave estrangeira para a tabela 'clientes'

    __table_args__ = (
        UniqueConstraint('ve_placa1', 've_estado_grupo', 've_status', name='uq_placa1_estado_grupo'),  # Define a restrição de unicidade composta
    )

class VistoriaImagens(Base):
    __tablename__ = 'vistoria_imagens'

    vi_id = Column(Integer, primary_key=True, autoincrement=True)  # ID único para cada registro
    vi_veiculo_id = Column(Integer, ForeignKey('veiculos.ve_id', ondelete='CASCADE'), nullable=False)  # Chave estrangeira para a tabela 'veiculos'
    vi_identificador = Column(String(50), nullable=False)  # Número da vistoria
    vi_status = Column(String(20), nullable=False) #
    vi_data_hora = Column(String, nullable=True)  # Data e hora da vistoria
    vi_nome = Column(String(255), nullable=True)  # Nome associado à vistoria
    vi_telefone = Column(String(20), nullable=True)  # Telefone associado à vistoria
    vi_caminho = Column(String, nullable=False)  # Caminhos das imagens (armazenados como JSON ou string delimitada)


# Criar as tabelas no banco de dados
Base.metadata.create_all(engine)