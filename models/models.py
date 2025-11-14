from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey, Float
from sqlalchemy.orm import declarative_base, relationship, mapped_column, Mapped
# from sqlalchemy_utils import ChoiceType

#Conexão com o banco de dados


db = create_engine(
    "sqlite:///.banco.db",
    connect_args={"check_same_thread": False},
    )

# Cria a base do banco de dados
Base = declarative_base()

# Criar as classes / tabelas do banco

class Usuario(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column("id", Integer, autoincrement=True, primary_key=True)
    nome: Mapped[str] = mapped_column("nome", String)
    email: Mapped[str] = mapped_column("email", String, nullable=False)
    senha: Mapped[str] = mapped_column("senha", String)
    ativo: Mapped[bool] = mapped_column("ativo", Boolean)
    admin: Mapped[bool] = mapped_column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo:bool=True, admin:bool=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin


class Pedido(Base):
    __tablename__ = "pedidos"

    # STATUS_PEDIDO = (
    #     ('PENDENTE', 'PENDENTE'),
    #     ('CANCELADO', 'CANCELADO'),
    #     ('FINALIZADO', 'FINALIZADO')
    # )

    id = Column("id", Integer, autoincrement=True, primary_key=True)
    status = Column("status", String) # pendente, cancelado, finalizado
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    preco = Column("preco", Float)
    itens = relationship("ItemPedido", cascade="all, delete")

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.usuario = usuario
        self.preco = preco
        self.status = status
    
    def calcular_preco(self):
        # percorrer todos os itens do pedido
        # somar todos os preços de todos os itens
        # editar no campo preco o valor final do preco do pedido

        # preco_pedido = 0
        # for item in self.itens:
        #     preco_item = item.preco_unitario * item.quantidade
        #     preco_pedido += preco_item

        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)


class ItemPedido(Base):
    __tablename__ = 'itens_pedido'

    id = Column("id", Integer, autoincrement=True, primary_key=True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido
    
# Executa a criação dos metadados do seu banco de dados

# Sempre que houver alterações na estrutura de qualquer entidade no banco de dados, devera ser executado a migração:
# Migração do banco de dados:
# alembic --revision --autogenerate -m ""
# alembic  upgrade head

