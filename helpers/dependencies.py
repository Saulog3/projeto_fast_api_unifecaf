from sqlalchemy.orm import sessionmaker
from models.models import db

def start_session():
    Session = sessionmaker(bind=db) #inicia uma sessão de query no db(engine)
    session = Session()

    return session