const formulario = document.getElementById("formulario-servico");
const mensagem = document.getElementById("mensagem-formulario");
const lista = document.getElementById("lista-servicos");
const estadoLista = document.getElementById("estado-lista");
const botaoSalvar = document.getElementById("botao-salvar");
const botaoCancelar = document.getElementById("botao-cancelar");
let nomesFornecedores = {};

async function carregarOpcoesFornecedores() {
    const fornecedores = await requisicaoApi("/api/fornecedores");
    const campo = document.getElementById("fornecedor-id");
    campo.replaceChildren();
    nomesFornecedores = {};
    fornecedores.forEach(function (item) {
        nomesFornecedores[item.id] = item.nome_comercial;
        const opcao = document.createElement("option");
        opcao.value = item.id;
        opcao.textContent = item.nome_comercial;
        campo.appendChild(opcao);
    });
}

function limparFormulario() {
    formulario.reset();
    document.getElementById("servico-id").value = "";
    document.getElementById("disponivel").checked = true;
    document.getElementById("titulo-formulario").textContent = "Novo serviço";
    botaoSalvar.textContent = "Salvar serviço";
    botaoCancelar.hidden = true;
}

function editarServico(item) {
    document.getElementById("servico-id").value = item.id;
    document.getElementById("fornecedor-id").value = item.fornecedor_id;
    document.getElementById("nome").value = item.nome;
    document.getElementById("descricao").value = item.descricao || "";
    document.getElementById("categoria").value = item.categoria;
    document.getElementById("preco-base").value = item.preco_base;
    document.getElementById("capacidade").value = item.capacidade_convidados;
    document.getElementById("disponivel").checked = item.disponivel;
    document.getElementById("titulo-formulario").textContent = "Editar serviço";
    botaoSalvar.textContent = "Atualizar serviço";
    botaoCancelar.hidden = false;
    window.scrollTo({ top: 0, behavior: "smooth" });
}

async function excluirServico(item) {
    if (!window.confirm(`Excluir o serviço ${item.nome}?`)) return;
    try { await requisicaoApi(`/api/servicos/${item.id}`, { method: "DELETE" }); mostrarMensagem(mensagem, "Serviço excluído.", "sucesso"); await carregarServicos(); }
    catch (erro) { mostrarMensagem(mensagem, erro.message, "erro"); }
}

async function carregarServicos() {
    estadoLista.textContent = "Carregando serviços...";
    lista.replaceChildren();
    try {
        await carregarOpcoesFornecedores();
        const itens = await requisicaoApi("/api/servicos");
        if (itens.length === 0) { estadoLista.textContent = "Nenhum serviço cadastrado."; return; }
        estadoLista.textContent = `${itens.length} serviço(s) encontrado(s).`;
        itens.forEach(function (item) {
            lista.appendChild(criarCartaoRegistro(item.nome, [nomesFornecedores[item.fornecedor_id] || `Fornecedor ${item.fornecedor_id}`, `${item.categoria} • R$ ${item.preco_base}`, `${item.capacidade_convidados} convidados • ${item.disponivel ? "Disponível" : "Indisponível"}`], function () { editarServico(item); }, function () { excluirServico(item); }));
        });
    } catch (erro) { estadoLista.textContent = `Erro: ${erro.message}`; }
}

async function salvarServico(evento) {
    evento.preventDefault();
    const id = document.getElementById("servico-id").value;
    const dados = { fornecedor_id: Number(document.getElementById("fornecedor-id").value), nome: document.getElementById("nome").value, descricao: document.getElementById("descricao").value, categoria: document.getElementById("categoria").value, preco_base: document.getElementById("preco-base").value, capacidade_convidados: Number(document.getElementById("capacidade").value), disponivel: document.getElementById("disponivel").checked };
    botaoSalvar.disabled = true;
    try { await requisicaoApi(id ? `/api/servicos/${id}` : "/api/servicos", { method: id ? "PUT" : "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(dados) }); mostrarMensagem(mensagem, id ? "Serviço atualizado." : "Serviço cadastrado.", "sucesso"); limparFormulario(); await carregarServicos(); }
    catch (erro) { mostrarMensagem(mensagem, erro.message, "erro"); } finally { botaoSalvar.disabled = false; }
}

formulario.addEventListener("submit", salvarServico);
botaoCancelar.addEventListener("click", limparFormulario);
document.getElementById("botao-atualizar").addEventListener("click", carregarServicos);
carregarServicos();
