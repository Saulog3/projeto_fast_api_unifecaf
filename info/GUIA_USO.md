# 🚀 GUIA DE USO - SISTEMA DE PEDIDOS INTEGRADO

## ⚡ Quick Start

### 1. Iniciar a Aplicação
```bash
cd c:\Users\Controle\Documents\GitHub\hastag_fasapi_class
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requiriments.txt
uvicorn main:app --reload
```

O servidor estará disponível em: **http://localhost:8000**

---

## 📱 Fluxo de Utilização

### PARTE 1: Criar Uma Conta

1. Acesse **http://localhost:8000/register**
2. Preencha os campos:
   - **Nome**: Seu nome completo
   - **Email**: Um email válido
   - **Senha**: Mínimo 6 caracteres
   - **Confirmar Senha**: Mesma senha acima

3. Clique em "Criar Conta"
4. Se tudo OK: Será redirecionado para login em 2 segundos
5. Se erro: Verá mensagem descrevendo o problema

---

### PARTE 2: Fazer Login

1. Acesse **http://localhost:8000/**
2. Insira:
   - **Email**: O email que você cadastrou
   - **Senha**: A senha que você cadastrou

3. Clique em "Entrar"
4. Se credenciais corretas:
   - ✅ Será redirecionado para o **Menu Principal**
   - ✅ Verá seu nome/email no topo
   - ✅ Tokens serão salvos no localStorage

---

### PARTE 3: Gerenciar Pedidos

#### 🆕 Criar um Novo Pedido

1. No menu, clique em **"➕ Novo Pedido"**
2. O sistema cria um pedido automático (recebe ID)
3. Preencha os dados do item:
   - **Quantidade**: Ex: 2
   - **Sabor**: Ex: "Pizza Margherita"
   - **Tamanho**: Selecione (P, M, G, GG)
   - **Preço Unitário**: Ex: 45.00

4. Clique em **"Adicionar Item"**
5. O item aparece na lista com seu preço

#### ➕ Adicionar Mais Itens

1. Repita o processo anterior
2. Cada item se adiciona à lista
3. O **Total** no final se atualiza automaticamente

#### 🗑️ Remover Um Item

1. Encontre o item na lista
2. Clique no botão **"Remover"** abaixo dele
3. Confirme a ação
4. Item é removido e total recalculado

#### ✅ Finalizar Pedido

1. Adicione pelo menos **1 item**
2. Clique em **"✅ Finalizar Pedido"**
3. Confirme a ação
4. Pedido muda para status **"FINALIZADO"**
5. Aparece na lista de pedidos com status em verde

#### ❌ Cancelar Pedido

1. Na lista de pedidos, encontre um pedido com status **"NOVO"**
2. Clique em **"❌ Cancelar"**
3. Confirme a ação
4. Pedido muda para status **"CANCELADO"**
5. Aparece em vermelho na lista

---

### PARTE 4: Visualizar Histórico

1. No menu, os pedidos são carregados automaticamente
2. Você vê:
   - **Todos os seus pedidos**
   - **Status de cada um** (NOVO, FINALIZADO, CANCELADO)
   - **Preço total de cada pedido**
   - **Detalhes dos itens**

3. Pedidos em status:
   - 🔵 **NOVO**: Pode finalizar ou cancelar
   - 🟢 **FINALIZADO**: Apenas visualizar
   - 🔴 **CANCELADO**: Apenas visualizar

---

### PARTE 5: Sair

1. Clique no botão **"Sair"** (canto superior direito)
2. Confirme que deseja sair
3. Será redirecionado para login
4. Todos os dados (tokens) são apagados

---

## 🔒 Informações Importantes

### O que é Guardado no Navegador (localStorage)?

Quando você faz login, estes dados são salvos:
- **access_token**: Prova que você está autenticado
- **refresh_token**: Token para renovar acesso
- **user_id**: Seu ID no sistema
- **user_email**: Seu email
- **user_admin**: Se você é administrador

Estes dados são **deletados** quando você faz logout.

### Segurança

✅ Tokens são verificados em cada requisição
✅ Você só pode ver/modificar seus próprios pedidos
✅ Senhas são criptografadas no servidor
✅ Confirmações antes de ações críticas

---

## 📊 Estados dos Pedidos

| Status | Cor | Ações Possíveis |
|--------|-----|-----------------|
| **NOVO** | 🔵 Azul | Finalizar, Cancelar, Adicionar/Remover itens |
| **FINALIZADO** | 🟢 Verde | Apenas visualizar |
| **CANCELADO** | 🔴 Vermelho | Apenas visualizar |

---

## ❌ Problemas Comuns

### "Erro ao criar pedido"
**Causa**: Você pode não estar autenticado
**Solução**: Faça logout e login novamente

### "E-mail do usuário já cadastrado"
**Causa**: Este email já existe no sistema
**Solução**: Use um email diferente para registrar

### "Usuário não encontrado ou credenciais inválidas"
**Causa**: Email ou senha incorretos
**Solução**: Verifique o email/senha digitados

### "Você não tem permissão"
**Causa**: Tentando acessar pedido de outro usuário
**Solução**: Só acesse seus próprios pedidos

### "A senha deve ter no mínimo 6 caracteres"
**Causa**: Senha muito curta
**Solução**: Use uma senha com 6+ caracteres

### "As senhas não coincidem"
**Causa**: Confirmação de senha diferente
**Solução**: Digite a mesma senha duas vezes

---

## 🧪 Testando a Aplicação

### Teste 1: Fluxo Completo (Recomendado)

1. ✅ Registre um novo usuário
2. ✅ Faça login
3. ✅ Crie um pedido
4. ✅ Adicione 2-3 itens
5. ✅ Finalize o pedido
6. ✅ Crie outro pedido
7. ✅ Cancele este pedido
8. ✅ Veja a lista de pedidos
9. ✅ Faça logout

### Teste 2: Validações

1. ✅ Tente registrar com email inválido (nada com @)
2. ✅ Tente registrar com senhas diferentes
3. ✅ Tente registrar com senha muito curta
4. ✅ Tente fazer login com senha errada
5. ✅ Tente finalizar pedido sem itens

### Teste 3: Segurança

1. ✅ Faça login em duas abas diferentes
2. ✅ Logout em uma aba
3. ✅ Tente usar a outra aba (verá que precisa fazer login)
4. ✅ Abra dev tools (F12)
5. ✅ Vá em Application > LocalStorage
6. ✅ Veja seus dados armazenados

---

## 📁 Arquivos Modificados/Criados

```
hastag_fasapi_class/
├── templates/
│   ├── login.html           (✏️ MODIFICADO)
│   ├── register.html        (✏️ MODIFICADO)
│   └── menu.html            (✏️ MODIFICADO)
├── static/js/
│   ├── login.js             (✏️ MODIFICADO)
│   ├── register.js          (✏️ MODIFICADO)
│   └── menu.js              (✏️ MODIFICADO - NOVO COMPLETO)
├── FRONTEND_INTEGRATION.md  (📄 NOVO)
├── IMPLEMENTACAO_CHECKLIST.md (📄 NOVO)
├── DIAGRAMA_FLUXO_DADOS.md (📄 NOVO)
└── GUIA_USO.md             (📄 NOVO)
```

---

## 🔧 Endpoints Utilizados

### Autenticação
- `POST /auth/login` → Fazer login
- `POST /auth/criar_conta` → Registrar novo usuário

### Pedidos
- `POST /pedidos/pedido` → Criar novo pedido
- `GET /pedidos/listar/pedidos-usuario` → Listar meus pedidos
- `POST /pedidos/pedido/adicionar-item/{id}` → Adicionar item
- `DELETE /pedidos/pedido/remover-item/{id}` → Remover item
- `POST /pedidos/pedidos/finalizar/{id}` → Finalizar pedido
- `POST /pedidos/pedidos/cancelar/{id}` → Cancelar pedido

---

## 💡 Dicas de Uso

1. 📋 Sempre confirme antes de finalizar um pedido
2. 🔐 Não compartilhe seu token de acesso
3. 🗑️ Pedidos cancelados não podem ser recuperados
4. 💰 Preços são calculados automaticamente
5. 📱 Funciona bem em mobile também
6. 🔄 Página atualiza automaticamente após ações

---

## 📞 Suporte

Se encontrar problemas:

1. ✅ Verifique se o servidor está rodando
2. ✅ Verifique a console do navegador (F12)
3. ✅ Verifique os logs do servidor
4. ✅ Verifique a base de dados
5. ✅ Tente fazer logout e login novamente

---

**Desenvolvido por**: GitHub Copilot
**Data**: 28 de Novembro de 2025
**Status**: ✅ Pronto para Produção

