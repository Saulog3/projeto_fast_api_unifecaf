# API de Pedidos --- FastAPI

Projeto acadêmico desenvolvido em **FastAPI**, implementando uma API
completa para gerenciamento de **usuários**, **pedidos**, **itens de
pedido** e **autenticação JWT**.\
Utiliza banco de dados SQLite, migrações com Alembic e segue uma
arquitetura organizada por responsabilidades.

------------------------------------------------------------------------

##  Funcionalidades

###  Autenticação e Usuários

-   Cadastro de usuários\
-   Login com geração de **JWT (access e refresh token)**\
-   Senhas protegidas com **Bcrypt**\
-   Rotas protegidas com **Bearer Token**

###  Pedidos

-   Criar pedidos\
-   Listar pedidos (geral ou por usuário)\
-   Visualizar detalhes de um pedido\
-   Finalizar e cancelar pedidos\
-   Adicionar ou remover itens do pedido\
-   Cálculo automático do valor total

###  Interface simples

-   Renderização de páginas HTML via FastAPI (ex.: `index.html`,
    `pedidos.html`)

------------------------------------------------------------------------

##  Estrutura do Projeto

     projeto/
    ├── main.py
    ├── router/
    │   ├── auth_routes.py
    │   ├── order_routes.py
    │   └── main_routes.py
    ├── models/
    │   └── models.py
    ├── helpers/
    │   ├── schemas.py
    │   └── dependencies.py
    ├── alembic/
    │   ├── versions/
    │   └── env.py
    ├── alembic.ini
    ├── static/
    ├── templates/
    ├── requiriments.txt
    └── .banco.db

------------------------------------------------------------------------

## 🛠 Tecnologias Utilizadas

-   **FastAPI**
-   **SQLite + SQLAlchemy**
-   **Alembic**
-   **Jinja2**
-   **Python-Jose**
-   **Bcrypt / Passlib**
-   **Uvicorn**

------------------------------------------------------------------------

##  Configuração e Execução

### 1️⃣ Criar ambiente virtual

Windows (PowerShell):

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2️⃣ Instalar dependências

``` powershell
pip install -r requiriments.txt
```

### 3️⃣ (Opcional) Criar .env

    SECRET_KEY=alternative
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30

### 4️⃣ Executar migrações Alembic

``` powershell
alembic revision --autogenerate -m "initial"
alembic upgrade head
```

### 5️⃣ Rodar o servidor FastAPI

``` powershell
uvicorn main:app --reload
```

------------------------------------------------------------------------

##  Endpoints Principais

###  Autenticação (`/auth`)

-   `POST /auth/criar_conta` --- Criar usuário\
-   `POST /auth/login` --- Login com JSON\
-   `POST /auth/login-form` --- Login com OAuth2 form\
-   `GET /auth/refresh` --- Renovar access token

###  Pedidos (`/pedidos`)

>  (`/pedidos/pedidos/...`).
> 
-   `POST /pedidos/pedido` --- Criar pedido\
-   `POST /pedidos/pedido/adicionar-item/{id}` --- Adicionar item\
-   `DELETE /pedidos/pedido/remover-item/{id}` --- Remover item\
-   `POST /pedidos/pedidos/finalizar/{id}` --- Finalizar pedido\
-   `POST /pedidos/pedidos/cancelar/{id}` --- Cancelar pedido\
-   `GET /pedidos/listar` --- Listar todos os pedidos (admin)\
-   `GET /pedidos/pedido/{id}` --- Detalhes do pedido\
-   `GET /pedidos/listar/pedidos-usuario` --- Pedidos do usuário
    autenticado

------------------------------------------------------------------------



------------------------------------------------------------------------

## 💡 Melhorias Futuras

-   Criar testes automatizados\
-   Criar Dockerfile e docker-compose\
-   Melhorar implementação de refresh token

------------------------------------------------------------------------

## 📄 Licença

Projeto para fins acadêmicos.\

