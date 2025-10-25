from fastapi import APIRouter, Depends
from models.models import Usuario
from helpers.dependencies import start_session

#APIRouter idica o o inicio do endpoint.
#Aqui será configurado tudo que tera no aaaa.aaaaaa.com/pedidos
auth_router = APIRouter(prefix="/auth", tags=['auth'])

@auth_router.get('/') # Aqui é definido a função que será executa na rota indicada
async def autenticação():
    """Essa é a rota padrão de atenticação do sistema"""
    return {"mensagem":" Você acessou a rota de autenticação", "autenticado": False}



@auth_router.post("/criar_conta")
async def criar_conta(email: str, senha: str, nome: str, session = Depends(start_session)):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if usuario: 
        # verifica se já existe um usuario com esse email
        return {"mensagem": "Já existe um usuario com esse email"}
    else:
        novo_usuario = Usuario(nome, email, senha)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": "Usuário cadastrado com sucesso"}

 