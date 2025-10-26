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
    id_usuario: int #O schema recebe o valor definido no models
   
    class Config:
        from_attributes = True


class LoginSchema(BaseModel):
    email: str
    senha: str
    
    class Config:
        from_attributes = True