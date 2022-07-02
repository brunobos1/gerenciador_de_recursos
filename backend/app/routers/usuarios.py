from fastapi import APIRouter, Body, Depends
from passlib.context import CryptContext
from app.models.model_usuarios import CriarUser, AlterarUser
from app.auth.auth_bearer import JWTBearer
import app.database.crud_usuarios as db_usr

router = APIRouter()

usuario_atual = ''

tipo_usuario = ''

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Cria a criptografia da senha
def get_password_hash(password):
    return pwd_context.hash(password)

@router.post("/usuarios/cadastrar", tags=["Usuarios"])
def cadastrar_usuario(user: CriarUser = Body(...)):

    try:
        consultar_usuario = db_usr.consultar_usuario_bd(user.usuario)
        if consultar_usuario != None:
            return {"mensagem": "Já existe um usuário com este login por favor tente outro."}
        
        user.senha = get_password_hash(user.senha)

        db_usr.criar_usuario_bd(user)

        usuario_novo = db_usr.consultar_usuario_bd(user.usuario)

        return {"mensagem": "Usuário criado com sucesso", "data": usuario_novo}
    
    except Exception as e:

        return {"mensagem": "Erro ao criar o usuario.", "erro": e}

@router.post("/usuarios/consultar", dependencies=[Depends(JWTBearer())], tags=["Usuarios"])
def consultar_usuario(usuario):

    try:
        consulta = db_usr.consultar_usuario_bd(usuario)

        return {"mensagem": "Sucesso na consulta", "data": consulta}
    
    except Exception as e:

        return {"mensagem": "Erro ao consultar o usuario.", "erro": e}

@router.get("/usuarios/listar", dependencies=[Depends(JWTBearer())], tags=["Usuarios"])
def listar_usuarios():

    try:
        consulta = db_usr.listar_usuarios_bd()

        return {"mensagem": "Sucesso na consulta", "data": consulta}
    
    except Exception as e:

        return {"mensagem": "Erro ao consultar lista de usuarios.", "erro": e}

@router.put("/usuarios/alterar", dependencies=[Depends(JWTBearer())], tags=["Usuarios"])
def alterar_usuario(usuario, user: AlterarUser = Body(...)):

    # try:

        consulta = db_usr.consultar_usuario_bd(usuario)
        if consulta == None:
            return {"mensagem": "Usuario não encontrado"}

        user.usuario = usuario

        if user.senha != '':
            user.senha = get_password_hash(user.senha)

        if user.nome == '': user.nome = consulta.nome
        if user.senha == '': user.senha = consulta.senha
        if user.tipo == '': user.tipo = consulta.tipo
        if user.status == '': user.status = consulta.status

        db_usr.alterar_usuario_bd(user)

        consulta_novo = db_usr.consultar_usuario_bd(usuario)

        return {"mensagem": "Usuario alterado com sucesso.", "data": consulta_novo}
    
    # except Exception as e:

    #     return {"mensagem": "Erro ao alterar o usuario.", "erro": e}

@router.delete("/usuarios/deletar", dependencies=[Depends(JWTBearer())], tags=["Usuarios"])
def deletar_usuario(usuario):

    try:
        db_usr.deletar_usuario_bd(usuario)

        consulta = db_usr.listar_usuarios_bd()

        for i in consulta:
            if i.usuario == usuario:
                return {"mensagem": "Ocorreu um erro ao excluir o usuario, por favor contate o suporte."}

        return {"mensagem": "Usuário excluido com sucesso!"}
    
    except Exception as e:

        return {"mensagem": "Erro ao excluir usuário.", "erro": e}