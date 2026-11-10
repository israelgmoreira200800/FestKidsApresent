const formulario = document.getElementById("formulario-festa");
const mensagem = document.getElementById("mensagem-formulario");
const lista = document.getElementById("lista-festas");
const estadoLista = document.getElementById("estado-lista");
const botaoSalvar = document.getElementById("botao-salvar");
const botaoCancelar = document.getElementById("botao-cancelar");
let nomesClientes = {};

async function carregarOpcoesClientes() {
    const clientes = await requisicaoApi("/api/clientes");
    const campo = document.getElementById("cliente-id");
    campo.replaceChildren();
    nomesClientes = {};
    clientes.forEach(function (item) {
        nomesClientes[item.id] = item.nome;
        const opcao = document.createElement("option");
        opcao.value = item.id;
        opcao.textContent = item.nome;
        campo.appendChild(opcao);
    });
}

function limparFormulario() {
    formulario.reset();
    document.getElementById("festa-id").value = "";
    document.getElementById("titulo-formulario").textContent = "Nova festa";
    botaoSalvar.textContent = "Salvar festa";
    botaoCancelar.hidden = true;
}

function editarFesta(item) {
    document.getElementById("festa-id").value = item.id;
    document.getElementById("cliente-id").value = item.cliente_id;
    document.getElementById("nome").value = item.nome;
    document.getElementById("data").value = item.data;
    document.getElementById("convidados").value = item.quantidade_convidados;
    document.getElementById("local").value = item.local;
    document.getElementById("orcamento").value = item.orcamento;
    document.getElementById("titulo-formulario").textContent = "Editar festa";
    botaoSalvar.textContent = "Atualizar festa";
    botaoCancelar.hidden = false;
    window.scrollTo({ top: 0, behavior: "smooth" });
}

async function excluirFesta(item) {
    if (!window.confirm(`Excluir a festa ${item.nome}?`)) return;
    try { await requisicaoApi(`/api/festas/${item.id}`, { method: "DELETE" }); mostrarMensagem(mensagem, "Festa excluída.", "sucesso"); await carregarFestas(); }
    catch (erro) { mostrarMensagem(mensagem, erro.message, "erro"); }
}

async function carregarFestas() {
    estadoLista.textContent = "Carregando festas...";
    lista.replaceChildren();
    try {
        await carregarOpcoesClientes();
        const itens = await requisicaoApi("/api/festas");
        if (itens.length === 0) { estadoLista.textContent = "Nenhuma festa cadastrada."; return; }
        estadoLista.textContent = `${itens.length} festa(s) encontrada(s).`;
        itens.forEach(function (item) {
            lista.appendChild(criarCartaoRegistro(item.nome, [nomesClientes[item.cliente_id] || `Cliente ${item.cliente_id}`, `${item.data} • ${item.quantidade_convidados} convidados`, `R$ ${item.orcamento} • ${item.status}`], function () { editarFesta(item); }, function () { excluirFesta(item); }));
        });
    } catch (erro) { estadoLista.textContent = `Erro: ${erro.message}`; }
}

async function salvarFesta(evento) {
    evento.preventDefault();
    const id = document.getElementById("festa-id").value;
    const dados = { cliente_id: Number(document.getElementById("cliente-id").value), nome: document.getElementById("nome").value, data: document.getElementById("data").value, local: document.getElementById("local").value, quantidade_convidados: Number(document.getElementById("convidados").value), orcamento: document.getElementById("orcamento").value };
    botaoSalvar.disabled = true;
    try { await requisicaoApi(id ? `/api/festas/${id}` : "/api/festas", { method: id ? "PUT" : "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(dados) }); mostrarMensagem(mensagem, id ? "Festa atualizada." : "Festa cadastrada.", "sucesso"); limparFormulario(); await carregarFestas(); }
    catch (erro) { mostrarMensagem(mensagem, erro.message, "erro"); } finally { botaoSalvar.disabled = false; }
}

formulario.addEventListener("submit", salvarFesta);
botaoCancelar.addEventListener("click", limparFormulario);
document.getElementById("botao-atualizar").addEventListener("click", carregarFestas);
carregarFestas();
