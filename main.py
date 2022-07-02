from fastapi import FastAPI, Body
from app.routers import usuarios, recursos
from app.schemas.schema_usuarios import UserLoginSchema
from passlib.context import CryptContext
from app.auth.auth_handler import signJWT
import app.database.crud_usuarios as db_usr

app = FastAPI(title='API Gerenciador de Recursos', version='0.0.1')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Compara a senha digitada com a senha criptografada
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Verifica se o usuario pode ter acesso ao token
def check_user(data: UserLoginSchema):
    check_usuarios = db_usr.listar_usuarios_bd()

    for u in check_usuarios:
        print(u)
        if u.usuario == data.usuario and verify_password(data.senha, u.senha) and u.status == 'Ativo' and u.tipo == 'administrador':
            return True

    return False

@app.get("/", tags=["Inicio"])
def comecar():

    return {"mensagem": "Olá, para usar a API no navegador adicione /docs na url."}

@app.post("/token", tags=["Login Administrativo"])
def login_administrador(user: UserLoginSchema = Body(...)):

    if check_user(user):

        consulta = db_usr.consultar_usuario_bd(user.usuario)
        global usuario_atual
        global tipo_usuario
        usuario_atual = user.usuario
        tipo_usuario = consulta.tipo
        return signJWT(user.usuario)

    return {"mensagem": "Login ou senha incorreto(s) ou você não tem acesso administrativo" }

app.include_router(usuarios.router)
app.include_router(recursos.router)