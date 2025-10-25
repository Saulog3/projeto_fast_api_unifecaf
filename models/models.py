from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey, Float
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils import ChoiceType

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


class Pedido(Base):
    __tablename__ = "pedidos"

    STATUS_PEDIDO = (
        ('PENDENTE', 'PENDENTE'),
        ('CANCELADO', 'CANCELADO'),
        ('FINALIZADO', 'FINALIZADO')
    )

    id = Column("id", Integer, autoincrement=True, primary_key=True)
    status = Column("status", ChoiceType(choices=STATUS_PEDIDO)) # pendente, cancelado, finalizado
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    preco = Column("preco", Float)
    # itens = Column("", )

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.usuario = usuario
        self.preco = preco
        self.status = status



# Executa a criação dos metadados do seu banco de dados