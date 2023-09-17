from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Endereco


class Cliente(Base):
    __tablename__ = 'cliente'

    id = Column("pk_cliente", Integer, primary_key=True)
    nome = Column(String(250), unique=True)
    cpf = Column(String(11), unique=True)
    data_nascimento = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o cliente e o endereco.
    # Essa relação é implicita, não está salva na tabela 'cliente',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    enderecos = relationship("Endereco")

    def __init__(self, nome:str, cpf:str, data_nascimento:Union[DateTime, None] = None):
        """
        Cria um Cliente

        Arguments:
            nome: nome do cliente.
            data_nascimento: data de quando o cliente nasceu
        """
        self.nome = nome
        self.cpf = cpf

        # se não for informada, será o data exata da inserção no banco
        if data_nascimento:
            self.data_nascimento = data_nascimento

    def adiciona_endereco(self, endereco:Endereco):
        """ Adiciona um novo endereço ao Cliente
        """
        self.enderecos.append(endereco)

