from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

templates = Jinja2Templates(directory="templates")
main_router = APIRouter()

@main_router.get("/", response_class=HTMLResponse)
def pagina_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@main_router.get("/pedidos", response_class=HTMLResponse)
def pagina_pedidos(request: Request):
    # não colocamos Depends(check_token) aqui porque a página HTML precisa ser exibida
    # e as requisições API que a página faça serão protegidas e validadas pelo backend.
    return templates.TemplateResponse("pedidos.html", {"request": request})
