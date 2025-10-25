from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey, Float
from sqlalchemy.orm import declarative_base

#Conexão com o banco de dados
db = create_engine("sqlite:///.banco.db")

# Cria a base do banco de dados
Base = declarative_base()

# Criar as classes / tabelas do banco

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column("id", Integer, autoincrement=True, primary_key=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin



# Executa a criação dos metadados do seu banco de dados