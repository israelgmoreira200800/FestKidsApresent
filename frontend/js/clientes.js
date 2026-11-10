const URL_API_CLIENTES = "http://127.0.0.1:5000/api/clientes";

const formulario = document.getElementById("formulario-cliente");
const botaoSalvar = document.getElementById("botao-salvar");
const mensagemFormulario = document.getElementById("mensagem-formulario");


function mostrarMensagem(texto, tipo) {
    mensagemFormulario.textContent = texto;
    mensagemFormulario.className = `mensagem ${tipo}`;
}


async function enviarCadastro(evento) {
    evento.preventDefault();

    const dados = {
        nome: document.getElementById("nome").value,
        email: document.getElementById("email").value,
        telefone: document.getElementById("telefone").value,
    };

    botaoSalvar.disabled = true;
    botaoSalvar.textContent = "Salvando...";
    mostrarMensagem("", "");

    try {
        const resposta = await fetch(URL_API_CLIENTES, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(dados),
        });

        const respostaDados = await resposta.json();

        if (!resposta.ok) {
            const mensagemErro = respostaDados.erro
                ? respostaDados.erro.mensagem
                : "Não foi possível cadastrar o cliente.";
            throw new Error(mensagemErro);
        }

        mostrarMensagem(
            `Cliente ${respostaDados.nome} cadastrado com o ID ${respostaDados.id}.`,
            "sucesso",
        );
        formulario.reset();
    } catch (erro) {
        mostrarMensagem(
            erro.message || "Não foi possível conectar à API.",
            "erro",
        );
    } finally {
        botaoSalvar.disabled = false;
        botaoSalvar.textContent = "Salvar cliente";
    }
}


formulario.addEventListener("submit", enviarCadastro);
