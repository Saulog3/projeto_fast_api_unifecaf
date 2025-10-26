from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioSchema(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    ativo: bool = True
    admin: bool = False
    
    class Config:
        from_attributes = True


class PedidoSchema(BaseModel):

    id_usuario: str #O schema recebe o valor definido no models

    
    class Config:
        from_attributes = True
