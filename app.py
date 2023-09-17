from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
from model import Cliente, Endereco
from logger import logger
from model import Session
from schemas import cliente, ClienteBuscaSchema, ClienteDelSchema, ClienteSchema, ClienteViewSchema, ListagemClientesSchema, ErrorSchema, apresenta_cliente, apresenta_clientes #*  UpdateClienteSchema
from flask_cors import CORS
from schemas.cliente import UpdateClienteSchema
from schemas.endereco import EnderecoSchema
import json

info = Info(title="Minha API - Clientes", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
cliente_tag = Tag(name="Cliente", description="Adição, visualização, atualização e remoção de clientes à base")
endereco_tag = Tag(name="Endereco", description="Adição de um endereço à um clientes cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi/swagger')


@app.post('/cliente', tags=[cliente_tag],
          responses={"200": ClienteViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_cliente(form: ClienteSchema):
    """Adiciona um novo Cliente à base de dados

    Retorna uma representação dos clientes e enderecos associados.
    """
    cliente = Cliente(
        nome=form.nome,
        cpf=form.cpf
        )
    logger.debug(f"Adicionando cliente de nome: '{cliente.nome}'")
    logger.debug(f"Adicionando cliente de nome: '{cliente}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando cliente
        session.add(cliente)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado cliente de nome: '{cliente.nome}'")
        return apresenta_cliente(cliente), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Cliente de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar cliente '{cliente.nome}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar cliente '{cliente.nome}', {error_msg}")
        return {"message": error_msg}, 400


@app.put('/update_cliente', tags=[cliente_tag],
          responses={"200": ClienteViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def update_cliente(form: UpdateClienteSchema):
    """Edita um Cliente já salvo na base de dados

    Retorna uma representação dos clientes e enderecos associados.
    """
    ## recebe o id ao invés do nome para busca
    id_cliente = form.id
    nome_cliente = form.nome
    cpf_cliente = form.cpf
    session = Session()

    try:
        #passa a buscar pelo id e o nome para possível troca
        #query = session.query(Cliente).filter(Cliente.nome == nome_veic)
        query = session.query(Cliente).filter(Cliente.id == id_cliente)
        print(query)
        db_cliente = query.first()
        if not db_cliente:
            # se o cliente não foi encontrado
            error_msg = "Cliente não encontrado na base :/"
            logger.warning(f"Erro ao buscar cliente '{nome_cliente}', {error_msg}")
            return {"message": error_msg}, 404
        else:
            '''if form.ano_fabricacao:
                db_cliente.ano_fabricacao = form.ano_fabricacao
            
            if form.ano_modelo_fabricacao:
                db_cliente.ano_modelo_fabricacao = form.ano_modelo_fabricacao
            
            if form.valor_diaria:
                db_cliente.valor_diaria = form.valor_diaria
            '''
            db_cliente.nome = form.nome # só para garantir, pois estava dando erro ao gravar o nome
            db_cliente.cpf = form.cpf
            session.add(db_cliente)
            session.commit()
            logger.debug(f"Alterado cliente de nome: '{db_cliente.nome}'")
            return apresenta_cliente(db_cliente), 200
        
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar cliente, {error_msg}")
        return {"message": error_msg}, 400
    

@app.get('/clientes', tags=[cliente_tag],
         responses={"200": ListagemClientesSchema, "404": ErrorSchema})
def get_clientes():
    """Faz a busca por todos os Cliente cadastrados

    Retorna uma representação da listagem de clientes.
    """
    logger.debug(f"Coletando clientes ")
    # criando conexão com a base
    session = Session()
    
    # fazendo a busca
    cursor = session.connection().connection.cursor

    # fazendo a busca pelo cliente
    #clientes = session.execute(f'Select * from cliente').fetchall()
    clientes = session.query(Cliente).all() #.order_by(Cliente.nome)
    print(clientes)

    if not clientes:
        # se não há clientes cadastrados
        return {"clientes": []}, 200
    else:
        logger.debug(f"%d clientes econtrados" % len(clientes))
        # retorna a representação de cliente
        return apresenta_clientes(clientes), 200


@app.get('/cliente', tags=[cliente_tag],
         responses={"200": ClienteViewSchema, "404": ErrorSchema})
def get_cliente(query: ClienteBuscaSchema):
    """Faz a busca por um Cliente a partir do id do cliente

    Retorna uma representação dos clientes e enderecos associados.
    """
    cliente_nome = query.nome
    cliente_cpf = query.cpf
    logger.debug(f"Coletando dados sobre cliente #{cliente_nome}")
    
    # criando conexão com a base
    session = Session()
    
    #
    #cursor = session.connection().connection.cursor

    # fazendo a busca pelo cliente por SQL
    #cliente = session.execute(f'Select * from cliente where cpf = {cliente_cpf} or nome= {cliente_nome}').fetchall()


    # fazendo a busca por 
    cliente = session.query(Cliente).filter(Cliente.nome == cliente_nome).first() # por nome
    #cliente = session.query(Cliente).filter(Cliente.cpf == cliente_cpf).first() # por cpf

    if not cliente:
        # se o cliente não foi encontrado
        error_msg = "Cliente não encontrado na base :/"
        logger.warning(f"Erro ao buscar cliente '{cliente_nome}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Cliente econtrado: '{cliente.nome}'")
        # retorna a representação de cliente
        return apresenta_cliente(cliente), 200


@app.delete('/cliente', tags=[cliente_tag],
            responses={"200": ClienteDelSchema, "404": ErrorSchema})
def del_cliente(query: ClienteBuscaSchema):
    """Deleta um Cliente a partir do nome de cliente informado

    Retorna uma mensagem de confirmação da remoção.
    """
    cliente_nome = unquote(unquote(query.nome))
    #cliente_cpf = unquote(unquote(query.cpf))

    #print(cliente_nome)
    logger.debug(f"Deletando dados sobre cliente #{cliente_nome}")
    
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Cliente).filter(Cliente.nome == cliente_nome).delete() # por nome
    #count = session.query(Cliente).filter(Cliente.cpf == cliente_cpf).delete() # por cpf
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado cliente #{cliente_nome}")
        return {"message": "Cliente removido", "Nome": cliente_nome}
    else:
        # se o cliente não foi encontrado
        error_msg = "Cliente não encontrado na base :/"
        logger.warning(f"Erro ao deletar cliente #'{cliente_nome}', {error_msg}")
        return {"message": error_msg}, 404


@app.post('/endereco', tags=[endereco_tag],
          responses={"200": ClienteViewSchema, "404": ErrorSchema})
def add_endereco(form: EnderecoSchema):
    """Adiciona de um novo endereço a um clientes cadastrado na base identificado pelo id

    Retorna uma representação dos clientes e endereço associados.
    """
    cliente_id  = form.cliente_id
    
    logger.debug(f"Adicionando endereço ao cliente #{cliente_id}")
    # criando conexão com a base
    session = Session()
    
    cursor = session.connection().connection.cursor

    # fazendo a busca pelo cliente
    cliente = session.execute(f'Select * from cliente where pk_cliente = {cliente_id}').fetchall()
    #logger.debug(f"Adicionado endereço ao cliente #{cliente.nome}")
    
    #cliente = session.query(Cliente).filter(Cliente.id == cliente_id).first()

    if not cliente:
        # se cliente não encontrado
        error_msg = "Cliente não encontrado na base :/"
        logger.warning(f"Erro ao adicionar endereco ao cliente '{cliente_id}', {error_msg}")
        #return {"message": error_msg}, 404
        return {"message": cliente}, 404


    # criando o endereço
    cep = form.cep
    logradouro = form.logradouro
    numero = form.numero
    bairro = form.bairro
    cidade = form.cidade
    estado = form.estado
    pais = form.pais

    endereco = Endereco(cep,logradouro,numero,bairro,cidade,estado,pais)
    #endereco = Endereco(logradouro)

 
    session.execute(f"""INSERT INTO endereco (cep,logradouro,numero,bairro,cidade,estado,pais,cliente) VALUES ('{cep}','{logradouro}','{numero}','{bairro}','{cidade}','{estado}','{pais}',{cliente_id});""") 
    #session.execute(f"""INSERT INTO endereco (cep,logradouro,numero,bairro,cidade,estado,pais,cliente) VALUES (?,?,?,?,?,?,?,?);""",(cep,logradouro,numero,bairro,cidade,estado,pais,cliente_id)) 
    session.commit()
 
    logger.debug(f"Adicionado endereço ao cliente #{cliente_id}")

    # retorna a representação de cliente

    return apresenta_cliente(form), 200