from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

#Conexão com o banco de dados
db = create_engine("sqlite:///.banco.db")

# Cria a base do banco de dados
Base = declarative_base()

# Criar as classes / tabelas do banco

class Usuario(Base):
    pass

# Executa a criação dos metadados do seu banco de dados