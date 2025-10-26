from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from helpers.schemas import PedidoSchema
from helpers.dependencies import start_session
from models.models import Pedido

#APIRouter idica o o inicio do endpoint.
#Aqui será configurado tudo que tera no aaaa.aaaaaa.com/pedidos
order_router = APIRouter(prefix="/pedidos", tags=['pedidos'])

@order_router.get('/') # Aqui é definido a função que será executa na rota indicada
async def pedidos():
    """Essa é a rota padrão de pedidos do sistema"""
    return {"mensagem":" Você acessou a rota de pedidos"}

@order_router.post('/pedido')
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(start_session)):
    novo_pedido = Pedido(usuario=PedidoSchema.id_usuario)
    session.add(novo_pedido)
    session.commit()
    return {'mensagem': f'O pedido {novo_pedido} foi registrado com sucesso'}
    