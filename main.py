# para rodar o nosso codigo, executar no terminal: uvicorn main:app --reload
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from passlib.context import CryptContext
from dotenv import load_dotenv
from typing import Final
import os

load_dotenv()

SECRET_KEY: Final[str] = os.getenv("SECRET_KEY") or 'alternative'
ALGORITHM: Final[str] =  os.getenv("ALGORITHM") or 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES =  int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


app = FastAPI()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory="static"), name="static")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl='auth/login-form')

from router.auth_routes import auth_router
from router.order_routes import order_router
from router.main_routes import main_router

app.include_router(auth_router)
app.include_router(order_router)
app.include_router(main_router)

