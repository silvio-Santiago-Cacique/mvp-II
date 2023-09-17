from pydantic import BaseModel
from typing import Optional, List
from model.cliente import Cliente

from schemas import EnderecoSchema


class ClienteSchema(BaseModel):
    """ Define como um novo cliente a ser inserido deve ser representado
    """
    nome: str = "juscelino kubitschek"
    cpf: str = "01234567890"

class ListagemClientesSchema(BaseModel):
    """ Define como uma listagem de clientes que será retornada.
    """
    clientes:List[ClienteSchema]


def apresenta_clientes(clientes: List[Cliente]):
    """ Retorna uma representação do cliente seguindo o schema definido em
        ClienteViewSchema.
    """
    
    result = []
    for cliente in clientes:
        result.append({
            "id": cliente.id,
            "nome": cliente.nome,
            "cpf":cliente.cpf,
            "total_enderecos": len(cliente.enderecos),
            "endereco": [{"Cep": c.cep, "Logradouro": c.logradouro,  "nº": c.numero,"Bairro": c.bairro,"Cidade": c.cidade,"Estado": c.estado,"País": c.pais }  for c in cliente.enderecos ]            
            
        })

    return {"clientes": result}

class ClienteBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do cliente.
    """
    nome: str = "juscelino kubitschek"
    cpf: str = "01234567890"


class ClienteViewSchema(BaseModel):
    """ Define como um cliente será retornado: cliente + acessórios.
    """
    id: int = 1
    nome: str = "juscelino kubitschek"
    cpf: str = "01234567890"
    total_enderecos: int = 1
    enderecos:List[EnderecoSchema]


class UpdateClienteSchema(BaseModel):
    """ Define como um novo cliente pode ser atualizado.
    """
    #inserido o id para facilitar a busca na base para alteração
    id:int = 1
    nome: str = "juscelino kubitschek"
    cpf: str = "01234567890"

    
class ClienteDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    nome: str
    cpf: str

def apresenta_cliente(cliente: Cliente):
    """ Retorna uma representação do cliente seguindo o schema definido em
        ClienteViewSchema.
    """
    print(cliente)
    return {
        "id": cliente.id,
        "nome": cliente.nome,
        "cpf": cliente.cpf,
        "total_endereco": len(cliente.enderecos),
        "endereco": [{"Cep": c.cep, "Logradouro": c.logradouro,  "nº": c.numero,"Bairro": c.bairro,"Cidade": c.cidade,"Estado": c.estado,"País": c.pais }  for c in cliente.enderecos ]
    }


