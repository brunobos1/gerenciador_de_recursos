from pydantic import BaseModel, Field

class UserLoginSchema(BaseModel):
    usuario: str = Field(...)
    senha: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "usuario": "jose21",
                "senha": "weakpassword"
            },
        }
    
class CriarUser(BaseModel):
    
    nome: str = Field(...)
    usuario: str = Field(...)
    senha: str = Field(...)
    tipo = 'usuario'
    status = 'Ativo'

    class Config:
        schema_extra = {
            "example": {
                "nome": "José Silva Cardoso",
                "usuario": "jose21",
                "senha": "weakpassword",
            }
        }

class CriarUserAdmin(BaseModel):
    
    nome: str = Field(...)
    usuario: str = Field(...)
    senha: str = Field(...)
    tipo = 'administrador'
    status = 'Ativo'

    class Config:
        schema_extra = {
            "example": {
                "nome": "José Silva Cardoso",
                "usuario": "jose21",
                "senha": "weakpassword",
                "tipo": 'administrador ou usuario',
                "status": 'Ativo ou Inativo'
            }
        }

class AlterarUser(BaseModel):
    
    nome = ''
    usuario = ''
    senha = ''
    tipo = ''
    status = 'Ativo'

    class Config:
        schema_extra = {
            "example": {
                "nome": "",
                "senha": "",
                "tipo": "",
                "status": ""
            }
        }
