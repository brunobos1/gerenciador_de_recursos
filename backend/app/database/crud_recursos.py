from .model_bd import Recurso_BD, Recursos, session
from datetime import datetime, timedelta

def criar_recurso_bd(resource: Recurso_BD):

    recurso = Recursos(id_usr=f'{resource.id_usr}', nome=f'{resource.nome}', versao=f'{resource.versao}', 
    codigo=f'{resource.codigo}', potencia=f'{resource.potencia}', data_inicio=f'{resource.data_inicio}', 
    data_fim=f'{resource.data_fim}')

    session.add(recurso)
    session.commit()

def consultar_recurso_bd(code):

    query_user = session.query(Recursos).filter_by(codigo=code).first()
    
    return query_user

def listar_recursos_bd():

    recursos = session.query(Recursos).order_by(Recursos.id).all()
    
    return recursos

def listar_recursos_disponiveis_bd():

    recursos = session.query(Recursos).order_by(Recursos.id).all()

    recursos_disponiveis = []

    FMT = '%d/%m/%Y %H:%M:%S'
    data_atual = datetime.now().strftime(FMT)
    
    for r in recursos:
        if datetime.strptime(r.data_fim, FMT) <= datetime.strptime(data_atual, FMT):
            recursos_disponiveis.append(r)
    
    return recursos_disponiveis

def alterar_recurso_bd(resource: Recurso_BD):

    recurso = session.query(Recursos).filter_by(codigo=resource.codigo).first()
    recurso.nome = resource.nome
    recurso.codigo = resource.codigo
    recurso.versao = resource.versao
    recurso.potencia = resource.potencia
    recurso.id_usr = resource.id_usr
    recurso.data_inicio = resource.data_inicio
    recurso.data_fim = resource.data_fim
    session.commit()

def deletar_recurso_bd(code):

    query_rsc = session.query(Recursos).filter_by(codigo=code).first()
    session.delete(query_rsc)
    session.commit()

def alocar_recurso_bd(id_usr: int, code):

    recurso = session.query(Recursos).filter_by(codigo=code).first()

    recurso.id_usr = id_usr 
    data_ini = datetime.now()
    recurso.data_inicio = data_ini.strftime('%d/%m/%Y %H:%M:%S')
    recurso.data_fim = (data_ini + timedelta(hours=1)).strftime('%d/%m/%Y %H:%M:%S')
    session.commit()

def desalocar_recurso_bd(code):

    recurso = session.query(Recursos).filter_by(codigo=code).first()

    recurso.id_usr = '' 
    recurso.data_inicio = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    recurso.data_fim = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    session.commit()