const form = document.getElementById("loginForm");
const msgErro = document.getElementById("msgErro");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;

    try {
        const response = await fetch("/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: email, senha: senha })
        });

        const data = await response.json();

        if (!response.ok) {
            msgErro.textContent = data.detail || "Erro ao autenticar";
            return;
        }

        // Tokens
        localStorage.setItem("access_token", data.access_token);
        localStorage.setItem("refresh_token", data.refresh_token);

        // Dados do usuário
        localStorage.setItem("user_id", data.usuario.id);
        localStorage.setItem("user_email", data.usuario.email);
        localStorage.setItem("user_admin", data.usuario.admin);

        // 👉 Agora redireciona SEMPRE para o menu
        window.location.href = "/menu";

    } catch (error) {
        msgErro.textContent = "Erro inesperado. Verifique o servidor.";
    }
});
