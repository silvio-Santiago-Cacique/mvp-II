from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# importando os elementos definidos no modelo
from model.base import Base
from model.endereco import Endereco
from model.cliente import Cliente


db_path = "database/"
# Verifica se o diretorio não existe
if not os.path.exists(db_path):
   # então cria o diretorio
   os.makedirs(db_path)

# url de acesso ao cliente (essa é uma url de acesso ao sqlite local)
db_url = 'sqlite:///%s/cliente.db' % db_path

# cria a engine de conexão com o cliente
engine = create_engine(db_url, echo=False)

# Instancia um criador de seção com o cliente
Session = sessionmaker(bind=engine)
#connection = engine.raw_connection()

# cria o cliente se ele não existir 
if not database_exists(engine.url):
    create_database(engine.url) 

# cria as tabelas do cliente, caso não existam
Base.metadata.create_all(engine)
