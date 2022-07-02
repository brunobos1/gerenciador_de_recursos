from .model_bd import User_BD, Usuarios, session

def criar_usuario_bd(user: User_BD):

    usuario = Usuarios(nome=f'{user.nome}', usuario=f'{user.usuario}', senha=f'{user.senha}', tipo=f'{user.tipo}', 
    status=f'{user.status}')

    session.add(usuario)
    session.commit()

def consultar_usuario_bd(usuario):

    query_user = session.query(Usuarios).filter_by(usuario=usuario).first()
    
    return query_user

def listar_usuarios_bd():

    usuarios = session.query(Usuarios).order_by(Usuarios.id).all()
    
    return usuarios

def alterar_usuario_bd(user: User_BD):

    usuario = session.query(Usuarios).filter_by(usuario=user.usuario).first()
    usuario.nome = user.nome
    usuario.senha = user.senha
    usuario.tipo = user.tipo
    usuario.status = user.status
    session.commit()

def deletar_usuario_bd(usuario):

    query_user = session.query(Usuarios).filter_by(usuario=usuario).first()
    session.delete(query_user)
    session.commit()

# criar_usuario_bd({'nome': 'Bruno Oliveira', 'usuario': 'brunobos1', 'senha': '$2b$12$kvgTb09SgwIjsum27a486ebL8phXBUqEqhtYuzxivL6RgUv0JTXF.', 'tipo': 'administrador', 'status': 'Ativo'})

# listar_usuarios_bd()