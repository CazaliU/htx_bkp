from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, JSON
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
class DadosClientes(Base):
    __tablename__ = 'clientes'
    id = Column('cl_id', Integer, primary_key=True, autoincrement=True)  # Alinha com a coluna cl_id no banco
    status = Column('cl_status', String, nullable=True)
    data_inclusao = Column('cl_data_inclusao', String, nullable=True)
    data_vigencia = Column('cl_data_vigencia', String, nullable=True)
    data_exclusao = Column('cl_data_exclusao', String, nullable=True)
    razao_social = Column('cl_razao_social', String, nullable=True)
    cnpj = Column('cl_cnpj', String, nullable=True)
    nome = Column('cl_nome', String, nullable=True)
    nacionalidade = Column('cl_nacionalidade', String, nullable=True)
    estado_civil = Column('cl_estado_civil', String, nullable=True)
    profissao = Column('cl_profissao', String, nullable=True)
    rg = Column('cl_rg', String, nullable=True)
    orgao_exp = Column('cl_orgao_exp', String, nullable=True)
    cpf = Column('cl_cpf', String, nullable=True)
    nascimento = Column('cl_nascimento', String, nullable=True)
    logradouro = Column('cl_logradouro', String, nullable=True)
    numero = Column('cl_numero', String, nullable=True)
    bairro = Column('cl_bairro', String, nullable=True)
    cep = Column('cl_cep', String, nullable=True)
    complemento = Column('cl_complemento', String, nullable=True)
    referencia = Column('cl_referencia', String, nullable=True)
    estado = Column('cl_estado', String, nullable=True)
    cidade = Column('cl_cidade', String, nullable=True)
    adm_logradouro = Column('cl_adm_logradouro', String, nullable=True)
    adm_numero = Column('cl_adm_numero', String, nullable=True)
    adm_bairro = Column('cl_adm_bairro', String, nullable=True)
    adm_cep = Column('cl_adm_cep', String, nullable=True)
    adm_complemento = Column('cl_adm_complemento', String, nullable=True)
    adm_referencia = Column('cl_adm_referencia', String, nullable=True)
    adm_estado = Column('cl_adm_estado', String, nullable=True)
    adm_cidade = Column('cl_adm_cidade', String, nullable=True)
    celular_preferencial = Column('cl_celular_preferencial', String, nullable=True)
    celular_complementar = Column('cl_celular_complementar', String, nullable=True)
    telefone = Column('cl_telefone', String, nullable=True)
    email = Column('cl_email', String, nullable=True)
    vigencia_contrato = Column('cl_vigencia_contrato', String, nullable=True)
    metodo_cobranca = Column('cl_metodo_cobranca', String, nullable=True)
    indice_participacao = Column('cl_indice_participacao', String, nullable=True)
    integracao_trackbrasil = Column('cl_integracao_trackbrasil', String, nullable=True)
    estado_grupo = Column('cl_estado_grupo', String, nullable=True)
    criado_em = Column('cl_criado_em', String, default="now()", nullable=True)

    __table_args__ = (
        UniqueConstraint('cl_cnpj', 'cl_cpf', 'cl_estado_grupo', name='uq_cnpj_cpf_estado_grupo'),  # Define a restrição de unicidade composta
    )


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
    # add lat/long
    vi_id = Column(Integer, primary_key=True, autoincrement=True)  # ID único para cada registro
    vi_veiculo_id = Column(Integer, ForeignKey('veiculos.ve_id', ondelete='CASCADE'), nullable=False)  # Chave estrangeira para a tabela 'veiculos'
    vi_identificador = Column(String(50), nullable=False)  # Número da vistoria
    vi_status = Column(String(20), nullable=False) #
    vi_data_hora = Column(String, nullable=True)  # Alterado para DateTime
    vi_nome = Column(String(255), nullable=True)  # Nome associado à vistoria
    vi_telefone = Column(String(20), nullable=True)  # Telefone associado à vistoria
    vi_caminho = Column(JSON, nullable=False)  # Caminhos das imagens (armazenados como JSON ou string delimitada)



class Sinistros(Base):
    __tablename__ = 'sinistros'

    si_id = Column(Integer, primary_key=True, autoincrement=True)  # ID único para cada sinistro
    si_codigo = Column(Integer, unique=True, nullable=False)  # Código único do sinistro
    si_cliente_id = Column(Integer, ForeignKey('clientes.cl_id', ondelete='CASCADE'), nullable=False)  # Chave estrangeira para a tabela 'clientes'
    si_veiculo_1 = Column(String, nullable=False)  # Veículo principal
    si_veiculo_2 = Column(String, nullable=True)  # Veículo adicional 1
    si_veiculo_3 = Column(String, nullable=True)  # Veículo adicional 2
    si_data_ocorrencia = Column(String, nullable=True)  # Data da ocorrência
    si_status = Column(String, nullable=True)  # Status do sinistro
    si_estado = Column(String, nullable=True)  # Estado do sinistro
    si_cidade = Column(String, nullable=True)  # Cidade do sinistro
    si_tipo = Column(String, nullable=True)  # Tipo do sinistro
    si_responsabilidade = Column(String, nullable=True)  # Responsabilidade do sinistro
    si_descricao_privada = Column(String, nullable=True)  # Descrição privada
    si_descricao_publica = Column(String, nullable=True)  # Descrição pública
    si_comunicante_nome = Column(String, nullable=True)  # Nome do comunicante
    si_comunicante_cidade = Column(String, nullable=True)  # Cidade do comunicante
    si_comunicante_estado = Column(String, nullable=True)  # Estado do comunicante
    si_comunicante_cpf = Column(String, nullable=True)  # CPF do comunicante
    si_comunicante_contato1 = Column(String, nullable=True)  # Contato 1 do comunicante
    si_comunicante_contato2 = Column(String, nullable=True)  # Contato 2 do comunicante
    si_comunicante_status = Column(String, nullable=True)  # Status do comunicante
    si_comunicante_primeiro_contato = Column(String, nullable=True)  # Primeiro contato do comunicante
    si_comunicante_narrativa = Column(String, nullable=True)  # Narrativa do comunicante
    si_andamento_processo_comunicacao_data_hora = Column(String, nullable=True)  # Data/hora da comunicação
    si_andamento_processo_comunicacao_obs_ = Column(String, nullable=True)  # Observação da comunicação
    si_andamento_processo_regulacao_data_hora = Column(String, nullable=True)  # Data/hora da regulação
    si_andamento_processo_regulacao_obs = Column(String, nullable=True)  # Observação da regulação
    si_andamento_processo_resolucao_data_hora = Column(String, nullable=True)  # Data/hora da resolução
    si_andamento_processo_resolucao_obs = Column(String, nullable=True)  # Observação da resolução
    si_andamento_processo_reforma_pagamento_data_hora = Column(String, nullable=True)  # Data/hora do pagamento da reforma
    si_andamento_processo_reforma_pagamento_obs = Column(String, nullable=True)  # Observação do pagamento da reforma
    si_andamento_processo_conclusao_data_hora = Column(String, nullable=True)  # Data/hora da conclusão
    si_andamento_processo_conclusao_obs = Column(String, nullable=True)  # Observação da conclusão
    si_andamento_processo_rateio = Column(String, nullable=True)  # Rateio do processo
    si_andamento_processo_status = Column(String, nullable=True)  # Status do processo
    si_caminho_anexos = Column(JSON, nullable=True)  # Caminhos dos anexos (armazenados como JSON)
    si_criado_em = Column(String, default="now()", nullable=True)  # Data de criação do registro
    

class Lancamentos(Base):
    __tablename__ = 'lancamentos'

    fi_id = Column(Integer, primary_key=True, autoincrement=True)  # ID único para cada lançamento
    fi_veiculo = Column(String, nullable=True)  # Veículo associado ao lançamento
    fi_integrante = Column(String, nullable=True)  # Integrante associado ao lançamento
    fi_operacao = Column(String, nullable=True)  # Operação realizada
    fi_conta = Column(String, nullable=True)  # Conta associada ao lançamento
    fi_situacao = Column(String, nullable=True)  # Situação do lançamento
    fi_data = Column(String, nullable=True)  # Data do lançamento
    fi_compensacao = Column(String, nullable=True)  # Data de compensação
    fi_tipo = Column(String, nullable=True)  # Tipo do lançamento
    fi_referente = Column(String, nullable=True)  # Referente ao lançamento
    fi_valor = Column(String, nullable=True)  # Valor do lançamento
    fi_obs = Column(String, nullable=True)  # Observações adicionais
    fi_anexos = Column(JSON, nullable=True)  # Anexos associados ao lançamento (armazenados como JSON)
    fi_criado_em = Column(String, default="now()", nullable=True)  # Data de criação do registro
    fi_cliente_id = Column(Integer, ForeignKey('clientes.cl_id', ondelete='SET NULL'), nullable=True)  # Chave estrangeira para a tabela 'clientes'
    fi_sinistro_codigo = Column(Integer, ForeignKey('sinistros.si_codigo', ondelete='SET NULL'), nullable=True)  # Chave estrangeira para a tabela 'sinistros'
