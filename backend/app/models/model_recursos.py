from pydantic import BaseModel, Field
from datetime import datetime

class CriarRecurso(BaseModel):
    
    nome: str = Field(...)
    codigo: str = Field(...)
    potencia: int = Field(...)
    versao: str = Field(...)
    data_inicio = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    data_fim = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    id_usr = ''

    class Config:
        schema_extra = {
            "example": {
                "nome": "Recurso 1",
                "codigo": "HS4561",
                "potencia": 6,
                "versao": "1.1.0.24",
            }
        }

class AlterarRecurso(BaseModel):
    
    id_usr = 0
    nome = ''
    codigo = ''
    versao = ''
    potencia = 0
    data_inicio = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    data_fim = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    class Config:
        schema_extra = {
            "example": {
                "id_usr": 0,
                "nome": "",
                "codigo": "",
                "versao": "",
                "potencia": 0
            }
        }