from pydantic import BaseModel


class EnderecoSchema(BaseModel):
    """ Define como um novo endereco a ser inserido deve ser representado
    """
    cliente_id: int = 1
    cep:str = "15000000"
    logradouro: str = "Av. Paulista"
    numero:str = "SN"
    bairro:str = "Centro"
    cidade:str = "São Paulo"
    estado:str = "São Paulo"
    pais:str = "Brasil"

