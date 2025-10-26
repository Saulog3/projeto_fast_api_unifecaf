# para rodar o nosso codigo, executar no terminal: uvicorn main:app --reload
from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from typing import Final

load_dotenv()

SECRET_KEY: Final[str] = os.getenv("SECRET_KEY") or 'alternative'
ALGORITHM: Final[str] =  os.getenv("ALGORITHM") or 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES =  int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from router.auth_routes import auth_router
from router.order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

