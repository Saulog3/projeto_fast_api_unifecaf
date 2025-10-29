from fastapi import APIRouter, Depends, HTTPException
from models.models import Usuario
from helpers.dependencies import start_session, check_token
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from helpers.schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError


#APIRouter idica o inicio do endpoint.
#Aqui será configurado tudo que tera no aaaa.aaaaaa.com/pedidos
auth_router = APIRouter(prefix="/auth", tags=['auth'])

def send_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {
        'sub': str(id_usuario),
        'exp': data_expiracao
    }
    jwt_enconde = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_enconde



def autenticar_usuario(email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario

@auth_router.get('/')
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
            usuario_schema.admin)
        
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"Usuário cadastrado com sucesso {usuario_schema.email}"}

@auth_router.post('/login')
async def login(login: LoginSchema, session: Session = Depends(start_session)):
    usuario = autenticar_usuario(login.email, login.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail='Usuário não encontrado ou credenciais inválidas')
    else:
        access_token = send_token(usuario.id)
        refresh_token = send_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }

@auth_router.get('/refresh')
async def use_refresh_token(usuario: Usuario = Depends(check_token)):
    access_token = send_token(usuario.id)
    return {
    "access_token": access_token,
    "token_type": "Bearer"
}