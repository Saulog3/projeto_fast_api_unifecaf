from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

main_router = APIRouter()

templates = Jinja2Templates(directory="templates")

@main_router.get("/")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@main_router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@main_router.get("/menu")
def menu_page(request: Request):
    return templates.TemplateResponse("menu.html", {"request": request})