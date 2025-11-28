document.getElementById("registerForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const nome = document.getElementById("nome").value;
    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;
    const confirmarSenha = document.getElementById("confirmarSenha").value;
    const msgElement = document.getElementById("msg");

    // Limpar mensagem anterior
    msgElement.textContent = "";
    msgElement.className = "";

    // Validar se as senhas são iguais
    if (senha !== confirmarSenha) {
        msgElement.textContent = "❌ As senhas não coincidem!";
        msgElement.className = "error";
        return;
    }

    // Validar comprimento mínimo de senha
    if (senha.length < 6) {
        msgElement.textContent = "❌ A senha deve ter no mínimo 6 caracteres!";
        msgElement.className = "error";
        return;
    }

    // Validar email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        msgElement.textContent = "❌ Email inválido!";
        msgElement.className = "error";
        return;
    }

    try {
        const res = await fetch("/auth/criar_conta", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                nome: nome,
                email: email, 
                senha: senha,
                ativo: true,
                admin: false
            })
        });

        const data = await res.json();

        if (!res.ok) {
            msgElement.textContent = "❌ " + (data.detail || "Erro ao cadastrar");
            msgElement.className = "error";
            return;
        }

        msgElement.textContent = "✅ Usuário criado com sucesso! Redirecionando para login...";
        msgElement.className = "success";
        
        // Limpar formulário
        document.getElementById("registerForm").reset();
        
        // Redirecionar para login após 2 segundos
        setTimeout(() => {
            window.location.href = "/";
        }, 2000);

    } catch (error) {
        msgElement.textContent = "❌ Erro inesperado. Verifique o servidor.";
        msgElement.className = "error";
        console.error(error);
    }
});
