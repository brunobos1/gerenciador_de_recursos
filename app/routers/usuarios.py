from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from passlib.context import CryptContext
from app.schemas.schema_usuarios import CriarUser, AlterarUser, CriarUserAdmin
from app.auth.auth_bearer import JWTBearer
import app.database.crud_usuarios as db_usr

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Cria a criptografia da senha
def get_password_hash(password):
    return pwd_context.hash(password)

@router.post("/usuarios/cadastrar", tags=["Usuarios"])
def cadastrar_usuario(user: CriarUser = Body(...)):

    try:
        consultar_usuario = db_usr.consultar_usuario_bd(user.usuario)
        if consultar_usuario != None:
            return JSONResponse(status_code=400,
            content={"mensagem": "Já existe um usuário com este login por favor tente outro."})
        
        if len(user.senha) < 6:
            return JSONResponse(status_code=400,
            content={"mensagem": "A senha deve conter pelo menos 6 caracteres"})
        
        if len(user.usuario) < 6:
            return JSONResponse(status_code=400,
            content={"mensagem": "O campo de usuário deve conter pelo menos 6 caracteres"})
        
        user.senha = get_password_hash(user.senha)
        
        if user.usuario == '' or user.senha == '' or user.nome == '':
            return JSONResponse(status_code=400,
            content={"mensagem": "Favor preencher todos os campos"})

        db_usr.criar_usuario_bd(user)

        usuario_novo = db_usr.consultar_usuario_bd(user.usuario)

        return {"mensagem": "Usuário criado com sucesso", "data": usuario_novo}
    
    except Exception as e:
        return JSONResponse(status_code=500,
        content={"mensagem": f"Erro ao tentar criar o usuario: {e}"})

@router.post("/usuarios/cadastrar_admin", dependencies=[Depends(JWTBearer())], tags=["Usuarios"])
def cadastrar_usuario_admin(user: CriarUserAdmin = Body(...)):

    try:
        consultar_usuario = db_usr.consultar_usuario_bd(user.usuario)
        if consultar_usuario != None:
            return JSONResponse(status_code=400,
            content={"mensagem": "Já existe um usuário com este login por favor tente outro."})
        
        if len(user.senha) < 6:
            return JSONResponse(status_code=400,
            content={"mensagem": "A senha deve conter pelo menos 6 caracteres"})
        
        if len(user.usuario) < 6:
            return JSONResponse(status_code=400,
            content={"mensagem": "O campo de usuário deve conter pelo menos 6 caracteres"})
        
        user.senha = get_password_hash(user.senha)

        if user.tipo != 'administrador' and user.tipo != 'usuario':
            return JSONResponse(status_code=400,
            content={"mensagem": "Tipo de usuario invalido, favor escolher entre 'administrador' ou 'usuario'."})
        
        if user.status != 'Ativo' and user.status != 'Inativo':
            return JSONResponse(status_code=400,
            content={"mensagem": "Status de usuario invalido, favor escolher entre 'Ativo' ou 'Inativo'."})

        if user.usuario == '' or user.senha == '' or user.nome == '':
            return JSONResponse(status_code=400,
            content={"mensagem": "Favor preencher todos os campos."})

        db_usr.criar_usuario_bd(user)

        usuario_novo = db_usr.consultar_usuario_bd(user.usuario)

        return {"mensagem": "Usuário criado com sucesso", "data": usuario_novo}
    
    except Exception as e:

        return JSONResponse(status_code=500,
        content={"mensagem": f"Ocorreu um erro ao tentar criar o usuário: {e}"})

@router.post("/usuarios/consultar", dependencies=[Depends(JWTBearer())], tags=["Usuarios"])
def consultar_usuario(usuario):

    try:
        consulta = db_usr.consultar_usuario_bd(usuario)

        return JSONResponse(status_code=200,
        content={"mensagem": "Sucesso na consulta", "data": consulta})
    
    except Exception as e:

        return JSONResponse(status_code=500,
        content={"mensagem": f"Ocorreu um erro ao tentar consultar o usuário: {e}"})

@router.get("/usuarios/listar", dependencies=[Depends(JWTBearer())], tags=["Usuarios"])
def listar_usuarios():

    try:
        consulta = db_usr.listar_usuarios_bd()

        return {"mensagem": "Sucesso na consulta", "data": consulta}
    
    except Exception as e:

        return JSONResponse(status_code=500,
        content={"mensagem": f"Ocorreu um erro ao tentar consultar a lista de usuários: {e}"})

@router.put("/usuarios/alterar", dependencies=[Depends(JWTBearer())], tags=["Usuarios"])
def alterar_usuario(usuario, user: AlterarUser = Body(...)):

    try:

        consulta = db_usr.consultar_usuario_bd(usuario)
        if consulta == None:
            return JSONResponse(status_code=404,
                                content={"mensagem": f"Usuário não encontrado."})

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
    
    except Exception as e:

        return JSONResponse(status_code=500,
        content={"mensagem": f"Ocorreu um erro ao tentar alterar o usuário: {e}"})

@router.delete("/usuarios/deletar", dependencies=[Depends(JWTBearer())], tags=["Usuarios"])
def deletar_usuario(usuario):

    try:
        db_usr.deletar_usuario_bd(usuario)

        consulta = db_usr.listar_usuarios_bd()

        for i in consulta:
            if i.usuario == usuario:
                return JSONResponse(status_code=500,
                content={"mensagem": "Ocorreu um erro ao tentar excluir o usuário, favor contatar o suporte."})

        return {"mensagem": "Usuário excluido com sucesso!"}
    
    except Exception as e:

        return JSONResponse(status_code=500,
        content={"mensagem": f"Ocorreu um erro ao tentar excluir o usuário: {e}"})