from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from helpers.schemas import PedidoSchema, ItemPedidoSchema, ResponseSchema
from helpers.dependencies import start_session, check_token
from models.models import Pedido, Usuario, ItemPedido
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List
import os

#APIRouter idica o o inicio do endpoint.
#Aqui será configurado tudo que tera no aaaa.aaaaaa.com/pedidos
order_router = APIRouter(prefix="/pedidos", tags=['pedidos'], dependencies=[Depends(check_token)])

@order_router.get('/') # Aqui é definido a função que será executa na rota indicada
async def pedidos():
    """Essa é a rota padrão de pedidos do sistema"""
    return {"mensagem":" Você acessou a rota de pedidos"}

@order_router.post('/pedido')
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(start_session)):
    novo_pedido = Pedido(usuario=pedido_schema.id_usuario)
    session.add(novo_pedido)
    session.commit()
    return {'mensagem': f'O pedido ID:{novo_pedido.id} registrado com sucesso'}

@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(start_session), usuario: Session = Depends(check_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()

    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")

    if usuario.id != pedido.usuario and not usuario.admin: # type: ignore
        raise HTTPException(status_code=401, detail="Você não tem permissão para fazer essa ação.")

    pedido.status = "CANCELADO" 
    session.commit()
    
    return{
        "mensagem": f"Pedido número: {pedido.id} cancelado com sucesso", 
        "pedido": pedido
    }
    
@order_router.get("/listar")
async def listar_pedidos(session: Session = Depends(start_session), usuario: Usuario = Depends(check_token)):
    if not getattr(usuario, "admin", True):
        raise HTTPException(status_code=401, detail="Você não tem permissão para fazer essa ação.")
    else:
        pedidos = session.query(Pedido).all()
        return{
            "pedidos": pedidos
        }

@order_router.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido(
    id_pedido: int,
    itens_pedido: ItemPedidoSchema, 
    session: Session = Depends(start_session),
    usuario: Usuario = Depends(check_token)):

    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if usuario.id != pedido.usuario and not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem permissão para fazer essa ação.")
    else:
        itens_pedido = ItemPedido(
            itens_pedido.quantidade,
            itens_pedido.sabor,
            itens_pedido.tamanho,
            itens_pedido.preco_unitario,
            id_pedido)
   
    session.add(itens_pedido)
    pedido.calcular_preco()
    session.commit()
    return{
        "mensagem:": "Item criado com sucesso",
        "item_id": itens_pedido.id,
        "preço_pedido": pedido.preco

    }

@order_router.delete("/pedido/remover-item/{id_item_pedido}")
async def remover_item_pedido(
    id_item_pedido: int,
    session: Session = Depends(start_session),
    usuario: Usuario = Depends(check_token)):

    item_pedido = session.query(ItemPedido).filter(ItemPedido.id==id_item_pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=400, detail="Item no pedido não encontrado")
    
    pedido = session.query(Pedido).filter(Pedido.id==item_pedido.pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    
    if usuario.id != pedido.usuario and not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem permissão para fazer essa ação.")
    
    session.delete(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return{
        "mensagem:": "Item removido com sucesso",
        "item_removido": item_pedido,
        "quantidade_itens_pedido": len(pedido.itens),
        "pedido": pedido
    }

@order_router.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido: int, session: Session = Depends(start_session), usuario: Session = Depends(check_token)): 
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()

    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")

    if usuario.id != pedido.usuario and not usuario.admin: # type: ignore
        raise HTTPException(status_code=401, detail="Você não tem permissão para fazer essa ação.")

    pedido.status = "FINALIZADO" 
    session.commit()
    
    return{
        "mensagem": f"Pedido número: {pedido.id} finalizado com sucesso", 
        "pedido": pedido
    }

@order_router.get("/pedido/{id_pedido}")
async def visualizar_pedido(
    id_pedido: int,
    session: Session = Depends(start_session),
    usuario: Usuario = Depends(check_token)):

    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem permissão para fazer essa modificação")
    return {
        'quantidade_itens_pedido': len(pedido.itens),
        'pedido': pedido
    }

@order_router.get("/listar/pedidos-usuario", response_model=List[ResponseSchema])
async def listar_pedidos_usuarios(
    session: Session = Depends(start_session), 
    usuario: Usuario = Depends(check_token)):
    pedidos = session.query(Pedido).filter(Pedido.usuario==usuario.id).all() # type: ignore
    return pedidos
