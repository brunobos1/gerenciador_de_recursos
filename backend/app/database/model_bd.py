from datetime import datetime
from email.policy import default
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

DATABASE_URL = 'mysql+pymysql://admin:bruno741123@database-1.coarjxirjuvt.sa-east-1.rds.amazonaws.com:3306/gerenciador_recursos'

engine = create_engine(DATABASE_URL)

Base = declarative_base()

class Usuarios(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    usuario = Column(String(100))
    senha = Column(String(100))
    tipo = Column(String(100), default='usuario')
    status = Column(String(100), default='Ativo')

    recursos = relationship('Recursos')

    def __repr__(self):
        retorno = f'id: {self.id}, nome: {self.nome}, usuario: {self.usuario}, senha: {self.senha}, tipo: {self.tipo}, status: {self.status}'
        return '{' + retorno + '}'

class Recursos(Base):
    __tablename__ = 'recursos'
    id = Column(Integer, primary_key=True)
    codigo = Column(String(10))
    nome = Column(String(100))
    versao = Column(String(100))
    potencia = Column(Integer)
    data_inicio = Column(String(20), default=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    data_fim = Column(String(20), default=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

    id_usr = Column(Integer, ForeignKey("usuarios.id"))

    def __repr__(self):
        retorno = f'id_usuario:{self.id_usr}, codigo: {self.codigo}, nome: {self.nome}, potencia: {self.potencia}, \
        versão: {self.versao}, data_inicio: {self.data_inicio}, data_fim: {self.data_fim}'
        return '{' + retorno + '}'

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

class User_BD(BaseModel):

    nome = ''
    usuario = ''
    senha = ''
    tipo = ''
    status= 'Ativo'

class Recurso_BD(BaseModel):

    id_usr= 1
    nome= ''
    codigo= ''
    versao= ''
    potencia= 0
    data_inicio= ''
    data_fim=''