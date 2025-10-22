from fastapi import APIRouter

#APIRouter idica o o inicio do endpoint.
#Aqui será configurado tudo que tera no aaaa.aaaaaa.com/pedidos
auth_router = APIRouter(prefix="/auth", tags=['auth'])

@auth_router.get('/') # Aqui é definido a função que será executa na rota indicada
async def autenticação():
    """Essa é a rota padrão de atenticação do sistema"""
    return {"mensagem":" Você acessou a rota de autenticação", "autenticado": False}