# para rodar o nosso codigo, executar no terminal: uvicorn main:app --reload
from fastapi import FastAPI

app = FastAPI()

from router.auth_routes import auth_router
from router.order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

