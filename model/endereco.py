from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from  model import Base


class Endereco(Base):
    __tablename__ = 'endereco'

    id = Column(Integer, primary_key=True, autoincrement=True)
    cep = Column(String(8))
    logradouro = Column(String(255))
    numero = Column(String(5))
    bairro = Column(String(50))
    cidade = Column(String(50))
    estado = Column(String(50))
    pais = Column(String(50))

    # Definição do relacionamento entre o Endereco e um cliente.
    # Aqui está sendo definido a coluna 'cliente' que vai guardar
    # a referencia ao cliente, a chave estrangeira que relaciona
    # um cliente ao Endereco.
    cliente = Column(Integer, ForeignKey("cliente.pk_cliente"), nullable=False)

    def __init__(self, cep:str, logradouro:str, numero:str, bairro:str, cidade:str, estado:str, pais:str):
    #def __init__(self, logradouro:str):
        """
        Cria um Endereco

        Arguments:
            logradouro: o logradouro de um Endereco.
            data_validade: data de quando o Endereco foi feito ou inserido
                           à base
        """
        self.cep = cep
        self.logradouro = logradouro
        self.numero = numero
        self.bairro = bairro
        self.cidade = cidade
        self.estado = estado
        self.pais = pais
        
