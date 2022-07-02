from fastapi import APIRouter, Body, Depends
from app.models.model_recursos import CriarRecurso, AlterarRecurso
from app.auth.auth_bearer import JWTBearer
from passlib.context import CryptContext
import app.database.crud_recursos as db_rsc
import app.database.crud_usuarios as db_usr
from datetime import datetime, timedelta

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Compara a senha digitada com a senha criptografada
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def check_user(usuario, senha):
    check_usuarios = db_usr.listar_usuarios_bd()

    for u in check_usuarios:
        if u.usuario == usuario and verify_password(senha, u.senha) and u.status == 'Ativo':
            return True

    return False

def check_resources():

    recursos = db_rsc.listar_recursos_bd()

    for r in recursos:
        if datetime.strptime(r.data_fim, '%d/%m/%Y %H:%M:%S') <= datetime.now():
            db_rsc.desalocar_recurso_bd(r.codigo)

@router.get("/recursos/listar_disponiveis", tags=["Recursos"])
def listar_recursos_disponiveis():
    check_resources()
    try:

        consulta = db_rsc.listar_recursos_disponiveis_bd()

        return {'mensagem': 'Sucesso na consulta', 'data': consulta}
    
    except Exception as e:

        return {"mensagem": "Erro ao consultar lista de recursos.", "erro": e}

@router.post("/recursos/alocar", tags=["Recursos"])
def alocar_recurso(usuario, senha, codigo_recurso):
    check_resources()

    if check_user(usuario, senha):
        consulta_rsc = db_rsc.consultar_recurso_bd(codigo_recurso)

        if datetime.strptime(consulta_rsc.data_fim, '%d/%m/%Y %H:%M:%S') > datetime.now():
            return {'mensagem': 'Falha na alocação, o recurso já está em uso'}

        consulta_usr = db_usr.consultar_usuario_bd(usuario)

        db_rsc.alocar_recurso_bd(consulta_usr.id, codigo_recurso)

        consulta_rsc_novo = db_rsc.consultar_recurso_bd(codigo_recurso)

        return {'mensagem': 'Sucesso na alocação de recurso', 'data': consulta_rsc_novo}
    
    return {'mensagem': 'Erro na alocação de recurso'}


@router.post("/recursos/cadastrar", dependencies=[Depends(JWTBearer())], tags=["Recursos"])
def registrar_recurso(resource: CriarRecurso = Body(...)):
    check_resources()
    try:
        consulta = db_rsc.consultar_recurso_bd(resource.codigo)
        if consulta != None:
            return {"mensagem": "Já existe um recurso com este código por favor tente outro."}

        db_rsc.criar_recurso_bd(resource)

        recurso_novo = db_rsc.consultar_recurso_bd(resource.codigo)

        return {"mensagem": "Recurso cadastrado com sucesso", "data": recurso_novo}
    
    except Exception as e:

        return {"mensagem": "Erro ao cadastrar recurso.", "erro": e}

@router.post("/recursos/consultar", dependencies=[Depends(JWTBearer())], tags=["Recursos"])
def consultar_recurso(codigo_recurso):
    check_resources()
    try:

        consulta = db_rsc.consultar_recurso_bd(codigo_recurso)

        return {'mensagem': 'Sucesso na consulta', 'data': consulta}
    
    except Exception as e:

        return {"mensagem": "Erro ao consultar lista de recursos.", "erro": e}

@router.get("/recursos/listar", dependencies=[Depends(JWTBearer())], tags=["Recursos"])
def listar_recursos():
    check_resources()
    try:

        consulta = db_rsc.listar_recursos_bd()

        return {'mensagem': 'Sucesso na consulta', 'data': consulta}
    
    except Exception as e:

        return {"mensagem": "Erro ao consultar lista de recursos.", "erro": e}

@router.put("/recursos/alterar", dependencies=[Depends(JWTBearer())], tags=["Recursos"])
def alterar_recurso(codigo_recurso, resource: AlterarRecurso = Body(...)):
    check_resources()
    try:

        consulta = db_rsc.consultar_recurso_bd(codigo_recurso)

        if consulta == None:
            return {"mensagem": "Não existe um recurso com este código"}

        if resource.nome == '': resource.nome = consulta.nome
        if resource.codigo == '': resource.codigo = consulta.codigo
        if resource.versao == '': resource.versao = consulta.versao
        if resource.potencia == 0: resource.potencia = consulta.potencia
        if resource.id_usr != 0:
            data_ini = datetime.now()
            resource.data_inicio = data_ini.strftime('%d/%m/%Y %H:%M:%S')
            resource.data_fim = (data_ini + timedelta(hours=1)).strftime('%d/%m/%Y %H:%M:%S')
        else:
            resource.id_usr = consulta.id_usr

        db_rsc.alterar_recurso_bd(resource)

        consulta_novo = db_rsc.consultar_recurso_bd(codigo_recurso)

        return {"mensagem": "Recurso alterado com sucesso.", "data": consulta_novo}
    
    except Exception as e:

        return {"mensagem": "Erro ao alterar o usuario.", "erro": e}

@router.put("/recursos/desalocar", dependencies=[Depends(JWTBearer())], tags=["Recursos"])
def desalocar_recurso(codigo_recurso):
    check_resources()
    try:

        db_rsc.desalocar_recurso_bd(codigo_recurso)

        consulta = db_rsc.consultar_recurso_bd(codigo_recurso)

        return {"mensagem": "Recurso excluido com sucesso!", "data": consulta}
    
    except Exception as e:

        return {"mensagem": "Erro ao excluir o recurso.", "erro": e}

@router.delete("/recursos/deletar", dependencies=[Depends(JWTBearer())], tags=["Recursos"])
def deletar_recurso(codigo_recurso):
    check_resources()
    try:

        db_rsc.deletar_recurso_bd(codigo_recurso)

        consulta = db_rsc.listar_recursos_bd()

        for i in consulta:
            if i.codigo == codigo_recurso:
                return {"mensagem": "Ocorreu um erro ao excluir o recurso, por favor contate o suporte."}

        return {"mensagem": "Recurso excluido com sucesso!"}
    
    except Exception as e:

        return {"mensagem": "Erro ao excluir o recurso.", "erro": e}