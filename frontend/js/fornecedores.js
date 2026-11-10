const formulario = document.getElementById("formulario-fornecedor");
const mensagem = document.getElementById("mensagem-formulario");
const lista = document.getElementById("lista-fornecedores");
const estadoLista = document.getElementById("estado-lista");
const botaoSalvar = document.getElementById("botao-salvar");
const botaoCancelar = document.getElementById("botao-cancelar");

function limparFormulario() {
    formulario.reset();
    document.getElementById("fornecedor-id").value = "";
    document.getElementById("disponivel").checked = true;
    document.getElementById("titulo-formulario").textContent = "Novo fornecedor";
    botaoSalvar.textContent = "Salvar fornecedor";
    botaoCancelar.hidden = true;
}

function editarFornecedor(item) {
    document.getElementById("fornecedor-id").value = item.id;
    document.getElementById("nome-comercial").value = item.nome_comercial;
    document.getElementById("email").value = item.email;
    document.getElementById("telefone").value = item.telefone;
    document.getElementById("disponivel").checked = item.disponivel;
    document.getElementById("titulo-formulario").textContent = "Editar fornecedor";
    botaoSalvar.textContent = "Atualizar fornecedor";
    botaoCancelar.hidden = false;
    window.scrollTo({ top: 0, behavior: "smooth" });
}

async function excluirFornecedor(item) {
    if (!window.confirm(`Excluir o fornecedor ${item.nome_comercial}?`)) return;
    try {
        await requisicaoApi(`/api/fornecedores/${item.id}`, { method: "DELETE" });
        mostrarMensagem(mensagem, "Fornecedor excluído com sucesso.", "sucesso");
        await carregarFornecedores();
    } catch (erro) { mostrarMensagem(mensagem, erro.message, "erro"); }
}

async function carregarFornecedores() {
    estadoLista.textContent = "Carregando fornecedores...";
    lista.replaceChildren();
    try {
        const itens = await requisicaoApi("/api/fornecedores");
        if (itens.length === 0) { estadoLista.textContent = "Nenhum fornecedor cadastrado."; return; }
        estadoLista.textContent = `${itens.length} fornecedor(es) encontrado(s).`;
        itens.forEach(function (item) {
            lista.appendChild(criarCartaoRegistro(item.nome_comercial, [item.email, item.telefone, item.disponivel ? "Disponível" : "Indisponível"], function () { editarFornecedor(item); }, function () { excluirFornecedor(item); }));
        });
    } catch (erro) { estadoLista.textContent = `Erro: ${erro.message}`; }
}

async function salvarFornecedor(evento) {
    evento.preventDefault();
    const id = document.getElementById("fornecedor-id").value;
    const dados = { nome_comercial: document.getElementById("nome-comercial").value, email: document.getElementById("email").value, telefone: document.getElementById("telefone").value, disponivel: document.getElementById("disponivel").checked };
    botaoSalvar.disabled = true;
    try {
        await requisicaoApi(id ? `/api/fornecedores/${id}` : "/api/fornecedores", { method: id ? "PUT" : "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(dados) });
        mostrarMensagem(mensagem, id ? "Fornecedor atualizado." : "Fornecedor cadastrado.", "sucesso");
        limparFormulario();
        await carregarFornecedores();
    } catch (erro) { mostrarMensagem(mensagem, erro.message, "erro"); } finally { botaoSalvar.disabled = false; }
}

formulario.addEventListener("submit", salvarFornecedor);
botaoCancelar.addEventListener("click", limparFormulario);
document.getElementById("botao-atualizar").addEventListener("click", carregarFornecedores);
carregarFornecedores();
