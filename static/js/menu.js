// Verificar se o usuário está autenticado
if (!localStorage.getItem("access_token")) {
    window.location.href = "/";
}

// Carregar dados do usuário
window.addEventListener("load", () => {
    const userName = localStorage.getItem("user_email") || "Usuário";
    document.getElementById("username").textContent = userName.split("@")[0];
    document.getElementById("useremail").textContent = userName;
    carregarPedidos();
});

// Variável para armazenar o ID do pedido em criação
let pedidoEmCriacao = null;
let itensTemporarios = [];

// Mostrar formulário de novo pedido
function mostrarNovoPedido() {
    criarNovoPedido();
}

// Esconder formulário de novo pedido
function esconderNovoPedido() {
    document.getElementById("novoPedidoSection").style.display = "none";
    pedidoEmCriacao = null;
    itensTemporarios = [];
    limparFormularioItem();
}

// Criar novo pedido na API
async function criarNovoPedido() {
    const userId = localStorage.getItem("user_id");
    const token = localStorage.getItem("access_token");

    try {
        const response = await fetch("/pedidos/pedido", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({ id_usuario: parseInt(userId) })
        });

        if (!response.ok) {
            alert("Erro ao criar pedido. Verifique se está autenticado.");
            return;
        }

        const data = await response.json();
        // Extrait o ID do pedido da mensagem
        const match = data.mensagem.match(/ID:(\d+)/);
        if (match) {
            pedidoEmCriacao = parseInt(match[1]);
            document.getElementById("novoPedidoId").textContent = pedidoEmCriacao;
            document.getElementById("novoPedidoSection").style.display = "block";
            itensTemporarios = [];
            atualizarListaItens();
        }
    } catch (error) {
        console.error("Erro:", error);
        alert("Erro ao criar pedido. Verifique o servidor.");
    }
}

// Adicionar item ao pedido
document.getElementById("adicionarItemForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const quantidade = parseInt(document.getElementById("quantidade").value);
    const sabor = document.getElementById("sabor").value;
    const tamanho = document.getElementById("tamanho").value;
    const preco_unitario = parseFloat(document.getElementById("preco_unitario").value);
    const token = localStorage.getItem("access_token");

    try {
        const response = await fetch(`/pedidos/pedido/adicionar-item/${pedidoEmCriacao}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                quantidade,
                sabor,
                tamanho,
                preco_unitario
            })
        });

        if (!response.ok) {
            const data = await response.json();
            alert("Erro: " + (data.detail || "Não foi possível adicionar o item"));
            return;
        }

        const data = await response.json();
        
        // Adicionar à lista temporária
        itensTemporarios.push({
            id: data.item_id,
            quantidade,
            sabor,
            tamanho,
            preco_unitario
        });

        // Atualizar UI
        atualizarListaItens();
        limparFormularioItem();
        alert("Item adicionado com sucesso!");

    } catch (error) {
        console.error("Erro:", error);
        alert("Erro ao adicionar item. Verifique o servidor.");
    }
});

// Atualizar lista de itens na tela
function atualizarListaItens() {
    const listItens = document.getElementById("listItens");
    let html = "";
    let total = 0;

    itensTemporarios.forEach((item, index) => {
        const subtotal = item.quantidade * item.preco_unitario;
        total += subtotal;
        html += `
            <div style="border: 1px solid #eee; padding: 10px; margin-bottom: 10px; border-radius: 3px;">
                <p><strong>${item.quantidade}x ${item.sabor}</strong> (${item.tamanho})</p>
                <p>R$ ${item.preco_unitario.toFixed(2)} unitário = R$ ${subtotal.toFixed(2)}</p>
                <button type="button" class="btn btn-danger" style="width: auto; padding: 5px 10px;" onclick="removerItem(${item.id})">Remover</button>
            </div>
        `;
    });

    listItens.innerHTML = html || "<p style='color: #999;'>Nenhum item adicionado ainda</p>";
    document.getElementById("precoTotal").textContent = total.toFixed(2);
}

// Remover item do pedido
async function removerItem(itemId) {
    if (!confirm("Tem certeza que deseja remover este item?")) return;

    const token = localStorage.getItem("access_token");

    try {
        const response = await fetch(`/pedidos/pedido/remover-item/${itemId}`, {
            method: "DELETE",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!response.ok) {
            alert("Erro ao remover item");
            return;
        }

        // Remover do array temporário
        itensTemporarios = itensTemporarios.filter(item => item.id !== itemId);
        atualizarListaItens();
        alert("Item removido com sucesso!");

    } catch (error) {
        console.error("Erro:", error);
        alert("Erro ao remover item");
    }
}

// Finalizar pedido
async function finalizarPedido() {
    if (itensTemporarios.length === 0) {
        alert("Adicione pelo menos um item ao pedido!");
        return;
    }

    if (!confirm("Tem certeza que deseja finalizar este pedido?")) return;

    const token = localStorage.getItem("access_token");

    try {
        const response = await fetch(`/pedidos/pedidos/finalizar/${pedidoEmCriacao}`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!response.ok) {
            const data = await response.json();
            alert("Erro: " + (data.detail || "Não foi possível finalizar o pedido"));
            return;
        }

        alert("✅ Pedido finalizado com sucesso!");
        esconderNovoPedido();
        carregarPedidos();

    } catch (error) {
        console.error("Erro:", error);
        alert("Erro ao finalizar pedido");
    }
}

// Limpar formulário de item
function limparFormularioItem() {
    document.getElementById("adicionarItemForm").reset();
}

// Carregar e exibir pedidos do usuário
async function carregarPedidos() {
    const token = localStorage.getItem("access_token");

    try {
        const response = await fetch("/pedidos/listar/pedidos-usuario", {
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!response.ok) {
            document.getElementById("listaPedidos").innerHTML = "<p>Erro ao carregar pedidos</p>";
            return;
        }

        const pedidos = await response.json();

        let html = "";
        if (pedidos.length === 0) {
            html = "<p style='text-align: center; color: #999;'>Você ainda não tem pedidos. <a href='javascript:mostrarNovoPedido()' style='cursor: pointer; color: #007bff;'>Crie um novo</a></p>";
        } else {
            pedidos.forEach(pedido => {
                const statusClass = `status-${pedido.status.toLowerCase()}`;
                let total = pedido.itens.reduce((sum, item) => sum + (item.quantidade * item.preco_unitario), 0);
                
                html += `
                    <div class="pedido-card">
                        <div class="pedido-header">
                            <div>
                                <strong>Pedido #${pedido.id}</strong>
                                <span class="status ${statusClass}">${pedido.status}</span>
                            </div>
                            <div style="text-align: right;">
                                <p style="margin: 0;">R$ ${total.toFixed(2)}</p>
                                <p style="font-size: 12px; color: #666; margin: 5px 0 0 0;">${pedido.itens.length} item(s)</p>
                            </div>
                        </div>
                        
                        <div style="max-height: 100px; overflow-y: auto; background: #f9f9f9; padding: 10px; border-radius: 3px; margin: 10px 0;">
                            ${pedido.itens.map(item => `
                                <p style="margin: 5px 0; font-size: 12px;">
                                    • ${item.quantidade}x ${item.sabor} (${item.tamanho}) - R$ ${(item.quantidade * item.preco_unitario).toFixed(2)}
                                </p>
                            `).join('')}
                        </div>

                        <div class="pedido-actions">
                            ${pedido.status === 'NOVO' ? `
                                <button class="btn btn-success" onclick="finalizarPedidoExistente(${pedido.id})">✅ Finalizar</button>
                                <button class="btn btn-danger" onclick="cancelarPedido(${pedido.id})">❌ Cancelar</button>
                            ` : ''}
                            ${pedido.status === 'FINALIZADO' || pedido.status === 'CANCELADO' ? `
                                <span style="padding: 8px; text-align: center;">Pedido ${pedido.status}</span>
                            ` : ''}
                        </div>
                    </div>
                `;
            });
        }

        document.getElementById("listaPedidos").innerHTML = html;

    } catch (error) {
        console.error("Erro:", error);
        document.getElementById("listaPedidos").innerHTML = "<p>Erro ao carregar pedidos</p>";
    }
}

// Finalizar pedido existente
async function finalizarPedidoExistente(pedidoId) {
    if (!confirm("Tem certeza que deseja finalizar este pedido?")) return;

    const token = localStorage.getItem("access_token");

    try {
        const response = await fetch(`/pedidos/pedidos/finalizar/${pedidoId}`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!response.ok) {
            alert("Erro ao finalizar pedido");
            return;
        }

        alert("✅ Pedido finalizado com sucesso!");
        carregarPedidos();

    } catch (error) {
        console.error("Erro:", error);
        alert("Erro ao finalizar pedido");
    }
}

// Cancelar pedido
async function cancelarPedido(pedidoId) {
    if (!confirm("Tem certeza que deseja cancelar este pedido?")) return;

    const token = localStorage.getItem("access_token");

    try {
        const response = await fetch(`/pedidos/pedidos/cancelar/${pedidoId}`, {
            method: "POST",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        if (!response.ok) {
            alert("Erro ao cancelar pedido");
            return;
        }

        alert("❌ Pedido cancelado com sucesso!");
        carregarPedidos();

    } catch (error) {
        console.error("Erro:", error);
        alert("Erro ao cancelar pedido");
    }
}

// Logout
function logout() {
    if (!confirm("Tem certeza que deseja sair?")) return;
    localStorage.clear();
    window.location.href = "/";
}