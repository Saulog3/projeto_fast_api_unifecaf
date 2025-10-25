from fastapi import APIRouter, Depends, HTTPException
from models.models import Usuario
from helpers.dependencies import start_session
from main import bcrypt_context
from helpers.schemas import UsuarioSchema
from sqlalchemy.orm import Session

#APIRouter idica o o inicio do endpoint.
#Aqui será configurado tudo que tera no aaaa.aaaaaa.com/pedidos
auth_router = APIRouter(prefix="/auth", tags=['auth'])

@auth_router.get('/') # Aqui é definido a função que será executa na rota indicada
async def autenticação():
    """Essa é a rota padrão de atenticação do sistema"""
    return {"mensagem":" Você acessou a rota de autenticação", "autenticado": False}

@auth_router.post("/criar_conta")

async def criar_conta(
    usuario_schema: UsuarioSchema,
    session: Session = Depends(start_session)
    ):

    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario: 
        # verifica se já existe um usuario com esse email
        raise HTTPException(status_code=400, detail="E-mail do usuário já cadastrado")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(
            usuario_schema.nome, 
            usuario_schema.email, 
            senha_criptografada, 
            usuario_schema.ativo, 
            usuario_schema.admin
            )
        
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"Usuário cadastrado com sucesso {usuario_schema.email}"}

 