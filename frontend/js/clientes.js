const formulario = document.getElementById("formulario-cliente");
const mensagem = document.getElementById("mensagem-formulario");
const lista = document.getElementById("lista-clientes");
const estadoLista = document.getElementById("estado-lista");
const botaoSalvar = document.getElementById("botao-salvar");
const botaoCancelar = document.getElementById("botao-cancelar");

function limparFormulario() {
    formulario.reset();
    document.getElementById("cliente-id").value = "";
    document.getElementById("titulo-formulario").textContent = "Novo cliente";
    botaoSalvar.textContent = "Salvar cliente";
    botaoCancelar.hidden = true;
}

function editarCliente(cliente) {
    document.getElementById("cliente-id").value = cliente.id;
    document.getElementById("nome").value = cliente.nome;
    document.getElementById("email").value = cliente.email;
    document.getElementById("telefone").value = cliente.telefone;
    document.getElementById("titulo-formulario").textContent = "Editar cliente";
    botaoSalvar.textContent = "Atualizar cliente";
    botaoCancelar.hidden = false;
    window.scrollTo({ top: 0, behavior: "smooth" });
}

async function excluirCliente(cliente) {
    if (!window.confirm(`Excluir o cliente ${cliente.nome}?`)) return;
    try {
        await requisicaoApi(`/api/clientes/${cliente.id}`, { method: "DELETE" });
        mostrarMensagem(mensagem, "Cliente excluído com sucesso.", "sucesso");
        await carregarClientes();
    } catch (erro) {
        mostrarMensagem(mensagem, erro.message, "erro");
    }
}

async function carregarClientes() {
    estadoLista.textContent = "Carregando clientes...";
    lista.replaceChildren();
    try {
        const clientes = await requisicaoApi("/api/clientes");
        if (clientes.length === 0) {
            estadoLista.textContent = "Nenhum cliente cadastrado.";
            return;
        }
        estadoLista.textContent = `${clientes.length} cliente(s) encontrado(s).`;
        clientes.forEach(function (cliente) {
            lista.appendChild(criarCartaoRegistro(
                cliente.nome,
                [cliente.email, cliente.telefone, `ID ${cliente.id}`],
                function () { editarCliente(cliente); },
                function () { excluirCliente(cliente); },
            ));
        });
    } catch (erro) {
        estadoLista.textContent = `Erro: ${erro.message}`;
    }
}

async function salvarCliente(evento) {
    evento.preventDefault();
    const id = document.getElementById("cliente-id").value;
    const dados = {
        nome: document.getElementById("nome").value,
        email: document.getElementById("email").value,
        telefone: document.getElementById("telefone").value,
    };
    botaoSalvar.disabled = true;
    try {
        await requisicaoApi(id ? `/api/clientes/${id}` : "/api/clientes", {
            method: id ? "PUT" : "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dados),
        });
        mostrarMensagem(mensagem, id ? "Cliente atualizado." : "Cliente cadastrado.", "sucesso");
        limparFormulario();
        await carregarClientes();
    } catch (erro) {
        mostrarMensagem(mensagem, erro.message, "erro");
    } finally {
        botaoSalvar.disabled = false;
    }
}

formulario.addEventListener("submit", salvarCliente);
botaoCancelar.addEventListener("click", limparFormulario);
document.getElementById("botao-atualizar").addEventListener("click", carregarClientes);
carregarClientes();
