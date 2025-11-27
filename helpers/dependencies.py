from sqlalchemy.orm import sessionmaker, Session
from main import SECRET_KEY, ALGORITHM
from models.models import db, Usuario
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer



oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")

def start_session():
    Session = sessionmaker(bind=db)
    session = None
    try:
        session = Session()
        yield session
    finally:
        if session is not None:
            session.close()

def check_token(token: str = Depends(oauth2_schema), session: Session = Depends(start_session)) -> Usuario:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        user_id = int(sub)
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Acesso Negado")

    usuario = session.query(Usuario).filter(Usuario.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Inválido")
    return usuario