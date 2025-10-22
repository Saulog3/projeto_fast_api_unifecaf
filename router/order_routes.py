from fastapi import APIRouter

#APIRouter idica o o inicio do endpoint.
#Aqui será configurado tudo que tera no aaaa.aaaaaa.com/pedidos
order_router = APIRouter(prefix="/pedidos", tags=['pedidos'])

@order_router.get('/') # Aqui é definido a função que será executa na rota indicada
async def pedidos():
    """Essa é a rota padrão de pedidos do sistema"""
    return {"mensagem":" Você acessou a rota de pedidos"}