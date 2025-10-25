from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioSchema(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    ativo: bool = True
    admin: bool = False
    
    class Config:
        orm_mode = True
