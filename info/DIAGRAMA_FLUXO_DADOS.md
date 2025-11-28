# 📊 DIAGRAMA DE FLUXO DE DADOS

## Fluxo 1: REGISTRO E LOGIN

```
┌─────────────────────────────────────────────────────────────────┐
│                    NOVO USUÁRIO                                 │
└─────────────────────────────────────────────────────────────────┘

1. REGISTRO
├─ Usuário acessa: http://localhost:8000/register
├─ Preenche: Nome, Email, Senha, Confirmar Senha
├─ Frontend valida dados (senhas, email)
├─ POST /auth/criar_conta com JSON:
│  {
│    "nome": "João Silva",
│    "email": "joao@email.com",
│    "senha": "senha123",
│    "ativo": true,
│    "admin": false
│  }
├─ Backend verifica se email já existe
├─ Se sim: Retorna erro 400
├─ Se não: Cria usuário, criptografa senha
├─ Retorna sucesso
└─ Frontend redireciona para login em 2s

2. LOGIN
├─ Usuário acessa: http://localhost:8000/
├─ Insere Email e Senha
├─ POST /auth/login com JSON:
│  {
│    "email": "joao@email.com",
│    "senha": "senha123"
│  }
├─ Backend autentica usuário
├─ Se válido: Gera tokens JWT
├─ Retorna resposta com:
│  {
│    "access_token": "eyJ0eXAi...",
│    "refresh_token": "eyJ0eXAi...",
│    "token_type": "Bearer",
│    "usuario": {
│      "id": 1,
│      "nome": "João Silva",
│      "email": "joao@email.com",
│      "admin": false
│    }
│  }
├─ Frontend armazena no localStorage:
│  • access_token
│  • refresh_token
│  • user_id: 1
│  • user_email: joao@email.com
│  • user_admin: false
└─ Redireciona para http://localhost:8000/menu
```

---

## Fluxo 2: CRIAR PEDIDO COM ITENS

```
┌─────────────────────────────────────────────────────────────────┐
│              CRIAR NOVO PEDIDO E ADICIONAR ITENS                │
└─────────────────────────────────────────────────────────────────┘

1. CRIAR PEDIDO
├─ Usuário clica em "➕ Novo Pedido"
├─ Frontend recupera dados:
│  • user_id = 1 (localStorage)
│  • token = "eyJ0eXAi..." (localStorage)
├─ POST /pedidos/pedido com:
│  {
│    "id_usuario": 1
│  }
├─ Header: Authorization: Bearer eyJ0eXAi...
├─ Backend verifica token (valida JWT)
├─ Cria novo pedido com status "NOVO"
├─ Retorna:
│  {
│    "mensagem": "O pedido ID:42 registrado com sucesso"
│  }
├─ Frontend extrai ID: 42
└─ Mostra formulário para adicionar itens

2. ADICIONAR ITEM #1
├─ Usuário preenche:
│  • Quantidade: 2
│  • Sabor: Pizza Margherita
│  • Tamanho: G
│  • Preço Unitário: 45.00
├─ POST /pedidos/pedido/adicionar-item/42 com:
│  {
│    "quantidade": 2,
│    "sabor": "Pizza Margherita",
│    "tamanho": "G",
│    "preco_unitario": 45.00
│  }
├─ Header: Authorization: Bearer eyJ0eXAi...
├─ Backend cria ItemPedido
├─ Calcula preço total do pedido
├─ Retorna:
│  {
│    "mensagem": "Item criado com sucesso",
│    "item_id": 101,
│    "preço_pedido": 90.00
│  }
├─ Frontend:
│  • Adiciona à lista local de itens
│  • Atualiza total: R$ 90.00
│  • Limpa formulário
└─ Usuário pode adicionar mais itens

3. ADICIONAR ITEM #2
├─ Usuário preenche:
│  • Quantidade: 1
│  • Sabor: Refrigerante
│  • Tamanho: 2L
│  • Preço Unitário: 12.00
├─ POST /pedidos/pedido/adicionar-item/42 com:
│  {
│    "quantidade": 1,
│    "sabor": "Refrigerante",
│    "tamanho": "2L",
│    "preco_unitario": 12.00
│  }
├─ Retorna item_id: 102
├─ Frontend:
│  • Adiciona novo item
│  • Atualiza total: R$ 102.00
└─ Pronto para finalizar

4. FINALIZAR PEDIDO
├─ Usuário clica "✅ Finalizar Pedido"
├─ Frontend confirma: "Tem certeza?"
├─ Se sim:
│  POST /pedidos/pedidos/finalizar/42
│  Header: Authorization: Bearer eyJ0eXAi...
├─ Backend:
│  • Verifica se usuário pode finalizar (permissão)
│  • Muda status para "FINALIZADO"
│  • Salva na base de dados
│  • Retorna:
│    {
│      "mensagem": "Pedido número: 42 finalizado com sucesso",
│      "pedido": {...}
│    }
├─ Frontend:
│  • Mostra sucesso
│  • Limpa formulário
│  • Recarrega lista de pedidos
└─ Pedido aparece em "Meus Pedidos" com status FINALIZADO
```

---

## Fluxo 3: LISTAR E GERENCIAR PEDIDOS

```
┌─────────────────────────────────────────────────────────────────┐
│            LISTAR E GERENCIAR PEDIDOS DO USUÁRIO                │
└─────────────────────────────────────────────────────────────────┘

1. CARREGAR LISTA DE PEDIDOS
├─ Usuário acessa menu
├─ Frontend faz: GET /pedidos/listar/pedidos-usuario
├─ Header: Authorization: Bearer eyJ0eXAi...
├─ Backend:
│  • Verifica token
│  • Identifica user_id = 1
│  • Query: SELECT * FROM Pedido WHERE usuario = 1
├─ Retorna lista:
│  [
│    {
│      "id": 42,
│      "status": "FINALIZADO",
│      "preco": 102.00,
│      "usuario": 1,
│      "itens": [
│        {
│          "quantidade": 2,
│          "sabor": "Pizza Margherita",
│          "tamanho": "G",
│          "preco_unitario": 45.00
│        },
│        {
│          "quantidade": 1,
│          "sabor": "Refrigerante",
│          "tamanho": "2L",
│          "preco_unitario": 12.00
│        }
│      ]
│    },
│    {
│      "id": 43,
│      "status": "NOVO",
│      "preco": 0.00,
│      "usuario": 1,
│      "itens": []
│    }
│  ]
├─ Frontend:
│  • Renderiza cards para cada pedido
│  • Pedido 42: FINALIZADO (verde), R$ 102.00, 2 itens
│  • Pedido 43: NOVO (azul), R$ 0.00, sem itens
│  • Mostra botões:
│    - Pedido 42: Sem botões (finalizado)
│    - Pedido 43: "✅ Finalizar" e "❌ Cancelar"
└─ Usuário pode interagir

2. CANCELAR PEDIDO
├─ Usuário vê Pedido 43 com status "NOVO"
├─ Clica em "❌ Cancelar"
├─ Frontend confirma: "Tem certeza?"
├─ Se sim:
│  POST /pedidos/pedidos/cancelar/43
│  Header: Authorization: Bearer eyJ0eXAi...
├─ Backend:
│  • Verifica permissão
│  • Muda status para "CANCELADO"
│  • Retorna sucesso
├─ Frontend:
│  • Mostra mensagem de sucesso
│  • Recarrega lista
└─ Pedido 43 agora mostra status "CANCELADO" (vermelho)

3. REMOVER ITEM (se pedido ainda em NOVO)
├─ Usuário vê Pedido 43 com itens
├─ Clica em "Remover" de um item
├─ Frontend confirma
├─ Se sim:
│  DELETE /pedidos/pedido/remover-item/101
│  Header: Authorization: Bearer eyJ0eXAi...
├─ Backend:
│  • Encontra ItemPedido 101
│  • Verifica permissão
│  • Deleta item
│  • Recalcula preço do pedido
├─ Frontend:
│  • Remove item da lista local
│  • Atualiza total
└─ Total do pedido reduz
```

---

## LocalStorage - Dados Persistentes

```javascript
// Após login bem-sucedido:
localStorage = {
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJz...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJz...",
  "user_id": "1",
  "user_email": "joao@email.com",
  "user_admin": "false"
}

// Verificação em cada requisição protegida:
if (!localStorage.getItem("access_token")) {
  // Usuário não autenticado
  window.location.href = "/"
}

// Todos os requests para /pedidos/* incluem:
headers = {
  "Authorization": "Bearer " + localStorage.getItem("access_token")
}
```

---

## Estrutura de Resposta de Pedidos

```json
{
  "id": 42,
  "status": "NOVO|FINALIZADO|CANCELADO",
  "preco": 102.00,
  "usuario": 1,
  "itens": [
    {
      "id": 101,
      "quantidade": 2,
      "sabor": "Pizza Margherita",
      "tamanho": "G",
      "preco_unitario": 45.00,
      "pedido": 42
    },
    {
      "id": 102,
      "quantidade": 1,
      "sabor": "Refrigerante",
      "tamanho": "2L",
      "preco_unitario": 12.00,
      "pedido": 42
    }
  ]
}
```

---

## Estados Possíveis do Pedido

```
NOVO
├─ Pode adicionar itens
├─ Pode remover itens
├─ Botão "Finalizar" disponível
├─ Botão "Cancelar" disponível
├─ Pode transitar para FINALIZADO
└─ Pode transitar para CANCELADO

FINALIZADO
├─ Sem modificações possíveis
├─ Mostra histórico
├─ Status verde
└─ Não pode voltar para NOVO

CANCELADO
├─ Sem modificações possíveis
├─ Mostra histórico
├─ Status vermelho
└─ Não pode voltar para NOVO
```

---

## Fluxo de Logout

```
1. Usuário clica "Sair"
2. Frontend confirma: "Tem certeza?"
3. Se sim:
   ├─ localStorage.clear()  // Remove tudo
   ├─ window.location.href = "/" // Volta para login
4. Próxima vez que acessar menu:
   ├─ Verifica if (!localStorage.getItem("access_token"))
   └─ Redireciona para login se vazio
```

---

## Segurança: Verificações em Cada Etapa

```
REGISTRO:
├─ Frontend: Valida formato de email
├─ Backend: Verifica se email já existe
└─ Backend: Criptografa senha com bcrypt

LOGIN:
├─ Frontend: Campos obrigatórios
├─ Backend: Valida credenciais
├─ Backend: Gera JWT token
└─ Frontend: Armazena com segurança

REQUISIÇÕES PROTEGIDAS (/pedidos/):
├─ Frontend: Verifica token no localStorage
├─ Frontend: Inclui token no header
├─ Backend: Valida JWT token
├─ Backend: Verifica se token não expirou
└─ Backend: Verifica permissões do usuário

AÇÕES DO USUÁRIO:
├─ Frontend: Confirmação antes de ações críticas
├─ Backend: Verifica se usuário é dono do pedido
├─ Backend: Verifica se usuário é admin
└─ Backend: Valida estado do pedido antes de transição
```

---

