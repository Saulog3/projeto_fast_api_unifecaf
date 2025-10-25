from sqlalchemy.orm import sessionmaker
from models.models import db

def start_session():
    Session = sessionmaker(bind=db)
    session = None
    try:
        session = Session()
        yield session
    finally:
        if session is not None:
            session.close()