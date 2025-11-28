# Integração Frontend com API FastAPI - Documentação

## Resumo das Mudanças Implementadas

### 1. Página de Login (`/templates/login.html` e `/static/js/login.js`)
✅ **Status**: Funcionando completamente

**Funcionalidades:**
- Formulário de login com email e senha
- Integração com endpoint `/auth/login`
- Armazenamento de tokens (access_token e refresh_token) no localStorage
- Armazenamento de dados do usuário (id, email, admin)
- Redirecionamento automático para `/menu` após login bem-sucedido
- Interface moderna com gradiente e animações

**Fluxo:**
1. Usuário insere email e senha
2. Requisição POST para `/auth/login`
3. Tokens e dados do usuário são salvos no localStorage
4. Redirecionamento para página de menu

---

### 2. Página de Registro (`/templates/register.html` e `/static/js/register.js`)
✅ **Status**: Funcionando completamente

**Funcionalidades:**
- Formulário com campos: Nome, Email, Senha, Confirmar Senha
- Validações no frontend:
  - Senhas devem coincidir
  - Mínimo 6 caracteres na senha
  - Email válido
- Integração com endpoint `/auth/criar_conta`
- Redirecionamento para login após registro bem-sucedido
- Interface moderna com gradiente

**Fluxo:**
1. Usuário preenche os 4 campos obrigatórios
2. Frontend valida os dados
3. Requisição POST para `/auth/criar_conta`
4. Sucesso: Mensagem de confirmação + redirecionamento para login (2 segundos)

---

### 3. Menu Principal (`/templates/menu.html` e `/static/js/menu.js`)
✅ **Status**: Totalmente integrado com API

**Funcionalidades:**

#### A. Gerenciamento de Pedidos
- **Criar novo pedido**: 
  - Clique em "Novo Pedido" abre formulário
  - Pedido é criado automaticamente na API
  - Recebe ID do pedido

- **Adicionar itens ao pedido**:
  - Campos: Quantidade, Sabor, Tamanho, Preço Unitário
  - Validação de dados
  - Cálculo automático de subtotais
  - Cada item adicionado integra com `/pedidos/pedido/adicionar-item/{id_pedido}`

- **Remover itens do pedido**:
  - Botão "Remover" para cada item
  - Integração com `/pedidos/pedido/remover-item/{id_item_pedido}`
  - Recalcula total automaticamente

- **Finalizar pedido**:
  - Validação: Deve ter pelo menos 1 item
  - Integração com `/pedidos/pedidos/finalizar/{id_pedido}`
  - Confirma antes de finalizar

- **Cancelar pedido**:
  - Integração com `/pedidos/pedidos/cancelar/{id_pedido}`
  - Confirma antes de cancelar

#### B. Listagem de Pedidos do Usuário
- Carrega automaticamente ao acessar a página
- Exibe:
  - ID do pedido
  - Status (NOVO, FINALIZADO, CANCELADO)
  - Preço total
  - Número de itens
  - Detalhes dos itens (quantidade, sabor, tamanho, preço)
- Integração com `/pedidos/listar/pedidos-usuario`

#### C. Segurança
- Verificação de autenticação ao carregar a página
- Todos os requests incluem o token Bearer no header
- Dados do usuário verificados no localStorage
- Função logout limpa dados e redireciona para login

#### D. Interface
- Design moderno e responsivo
- Cores e estados visuais diferentes para cada status
- Animações suaves
- Layout em cards para melhor visualização

---

## Endpoints da API Utilizados

### Autenticação
- `POST /auth/login` - Login do usuário
- `POST /auth/criar_conta` - Registro de novo usuário

### Pedidos
- `POST /pedidos/pedido` - Criar novo pedido
- `GET /pedidos/listar/pedidos-usuario` - Listar pedidos do usuário logado
- `POST /pedidos/pedido/adicionar-item/{id_pedido}` - Adicionar item ao pedido
- `DELETE /pedidos/pedido/remover-item/{id_item_pedido}` - Remover item do pedido
- `POST /pedidos/pedidos/finalizar/{id_pedido}` - Finalizar pedido
- `POST /pedidos/pedidos/cancelar/{id_pedido}` - Cancelar pedido

---

## Fluxo Completo de Uso

### 1. Novo Usuário
1. Acessa `/register`
2. Preenche: Nome, Email, Senha, Confirmar Senha
3. Clica em "Criar Conta"
4. Sistema valida e cria usuário
5. Redireciona para `/` (login) após 2 segundos
6. Usuário faz login com email e senha

### 2. Usuário Autenticado
1. Login bem-sucedido → redireciona para `/menu`
2. Menu carrega automaticamente todos os pedidos do usuário
3. Pode criar novo pedido:
   - Clica em "Novo Pedido"
   - Adiciona múltiplos itens
   - Finaliza o pedido
4. Pode gerenciar pedidos existentes:
   - Finalizar pedido em status "NOVO"
   - Cancelar pedido em status "NOVO"
   - Ver histórico de pedidos finalizados/cancelados
5. Logout limpa tudo e volta para login

---

## LocalStorage - Dados Armazenados

Após login bem-sucedido:
```javascript
localStorage.setItem("access_token", token)        // Token de autenticação
localStorage.setItem("refresh_token", token)       // Token de atualização
localStorage.setItem("user_id", userId)            // ID do usuário
localStorage.setItem("user_email", userEmail)      // Email do usuário
localStorage.setItem("user_admin", isAdmin)        // Flag de admin
```

---

## Tecnologias Utilizadas

- **Frontend**: HTML5, CSS3, JavaScript Vanilla
- **API**: FastAPI (Python)
- **Autenticação**: JWT (Bearer Token)
- **Requisições**: Fetch API
- **Armazenamento**: Browser LocalStorage

---

## Validações Implementadas

### Registro
- ✅ Email válido
- ✅ Senhas coincidem
- ✅ Mínimo 6 caracteres na senha

### Login
- ✅ Email e senha obrigatórios
- ✅ Verificação no servidor

### Pedidos
- ✅ Mínimo 1 item para finalizar
- ✅ Token de autenticação em todas as requisições
- ✅ Confirmação antes de ações críticas

---

## Notas Importantes

1. **Token no Header**: Todos os requests para `/pedidos/*` incluem:
   ```javascript
   "Authorization": `Bearer ${token}`
   ```

2. **Segurança**: O frontend verifica autenticação antes de acessar páginas protegidas

3. **Responsividade**: Interface funciona bem em desktop e mobile

4. **Tratamento de Erros**: Mensagens claras para cada tipo de erro

5. **UX**: Confirmações antes de ações destrutivas (cancelar, remover)

---

## Como Testar

### 1. Iniciar a aplicação
```bash
uvicorn main:app --reload
```

### 2. Acessar
- Login: `http://localhost:8000/`
- Registro: `http://localhost:8000/register`
- Menu: `http://localhost:8000/menu` (após login)

### 3. Fluxo de teste
1. Registrar novo usuário
2. Fazer login
3. Criar novo pedido
4. Adicionar 2-3 itens
5. Finalizar pedido
6. Criar outro pedido e cancelar
7. Verificar listagem de pedidos
8. Fazer logout

---

## Próximas Melhorias Possíveis

- [ ] Página de perfil do usuário
- [ ] Histórico de pedidos com filtros
- [ ] Edição de dados de perfil
- [ ] Upload de avatar
- [ ] Notificações em tempo real
- [ ] Integração com sistema de pagamento
- [ ] Relatórios de pedidos (admin)
- [ ] Dashboard administrativo

