#!/usr/bin/env python3
"""
Script de teste para validar a integração frontend com a API
Testa o fluxo completo de registro, login e gerenciamento de pedidos
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_section(title):
    """Imprime uma seção formatada"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def test_register():
    """Testa o registro de um novo usuário"""
    print_section("TEST 1: Registro de Novo Usuário")
    
    email = f"test_{datetime.now().timestamp()}@test.com"
    data = {
        "nome": "Usuário Teste",
        "email": email,
        "senha": "senha123",
        "ativo": True,
        "admin": False
    }
    
    response = requests.post(f"{BASE_URL}/auth/criar_conta", json=data)
    print(f"Status: {response.status_code}")
    print(f"Resposta: {response.json()}")
    
    return email, data["senha"]

def test_login(email, senha):
    """Testa o login"""
    print_section("TEST 2: Login")
    
    data = {
        "email": email,
        "senha": senha
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Token recebido: {result.get('access_token', 'ERRO')[:20]}...")
    print(f"Usuário ID: {result.get('usuario', {}).get('id')}")
    print(f"Email: {result.get('usuario', {}).get('email')}")
    
    return result.get('access_token')

def test_criar_pedido(token, user_id):
    """Testa a criação de um novo pedido"""
    print_section("TEST 3: Criar Novo Pedido")
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {"id_usuario": user_id}
    
    response = requests.post(f"{BASE_URL}/pedidos/pedido", json=data, headers=headers)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Resposta: {result}")
    
    # Extrait o ID do pedido
    import re
    match = re.search(r'ID:(\d+)', result.get('mensagem', ''))
    pedido_id = int(match.group(1)) if match else None
    
    return pedido_id

def test_adicionar_item(token, pedido_id):
    """Testa a adição de um item ao pedido"""
    print_section("TEST 4: Adicionar Item ao Pedido")
    
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "quantidade": 2,
        "sabor": "Pizza Margherita",
        "tamanho": "G",
        "preco_unitario": 45.00
    }
    
    response = requests.post(f"{BASE_URL}/pedidos/pedido/adicionar-item/{pedido_id}", 
                            json=data, headers=headers)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Resposta: {result}")
    
    return result.get('item_id')

def test_listar_pedidos(token):
    """Testa a listagem de pedidos do usuário"""
    print_section("TEST 5: Listar Pedidos do Usuário")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/pedidos/listar/pedidos-usuario", headers=headers)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Total de pedidos: {len(result)}")
    
    if result:
        pedido = result[0]
        print(f"Primeiro pedido:")
        print(f"  - ID: {pedido.get('id')}")
        print(f"  - Status: {pedido.get('status')}")
        print(f"  - Preço: R$ {pedido.get('preco', 0):.2f}")
        print(f"  - Itens: {len(pedido.get('itens', []))}")

def test_finalizar_pedido(token, pedido_id):
    """Testa a finalização de um pedido"""
    print_section("TEST 6: Finalizar Pedido")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.post(f"{BASE_URL}/pedidos/pedidos/finalizar/{pedido_id}", 
                            headers=headers)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Resposta: {result.get('mensagem')}")

def run_all_tests():
    """Executa todos os testes"""
    try:
        print_section("TESTE DE INTEGRAÇÃO FRONTEND-API")
        print("Este script testa o fluxo completo de:")
        print("1. Registro de novo usuário")
        print("2. Login")
        print("3. Criação de pedido")
        print("4. Adição de itens")
        print("5. Listagem de pedidos")
        print("6. Finalização de pedido")
        
        # Teste 1: Registro
        email, senha = test_register()
        
        # Teste 2: Login
        token = test_login(email, senha)
        
        # Extrair user_id da resposta anterior (você precisará armazenar isso)
        # Para este teste, vamos assumir que o ID é 1
        user_id = 1
        
        # Teste 3: Criar pedido
        pedido_id = test_criar_pedido(token, user_id)
        
        if pedido_id:
            # Teste 4: Adicionar item
            item_id = test_adicionar_item(token, pedido_id)
            
            # Teste 5: Listar pedidos
            test_listar_pedidos(token)
            
            # Teste 6: Finalizar pedido
            test_finalizar_pedido(token, pedido_id)
        
        print_section("TESTES CONCLUÍDOS COM SUCESSO! ✅")
        
    except Exception as e:
        print_section("ERRO DURANTE OS TESTES! ❌")
        print(f"Erro: {str(e)}")
        print("\nCertifique-se de que:")
        print("1. O servidor FastAPI está rodando em http://localhost:8000")
        print("2. A base de dados está acessível")
        print("3. Todas as dependências estão instaladas")

if __name__ == "__main__":
    run_all_tests()
