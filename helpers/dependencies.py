from sqlalchemy.orm import sessionmaker, Session
from main import SECRET_KEY, ALGORITHM, oauth2_schema
from models.models import db, Usuario
from fastapi import Depends, HTTPException
from jose import jwt, JWTError


def start_session():
    Session = sessionmaker(bind=db)
    session = None
    try:
        session = Session()
        yield session
    finally:
        if session is not None:
            session.close()

def check_token(token: str = Depends(oauth2_schema), session: Session = Depends(start_session)):
    try:
        dicionario_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = dicionario_info.get('sub')
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso Negado")
    # Verificar se o token é válido
    # Extrair o id do usuário do token
    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Inválido")
    return usuario