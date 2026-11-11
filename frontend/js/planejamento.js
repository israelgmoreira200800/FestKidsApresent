const linksEtapas = Array.from(document.querySelectorAll("[data-etapa]"));
const paineisEtapas = Array.from(document.querySelectorAll("[data-painel]"));
const estadoEtapa = document.getElementById("estado-etapa");
const seletorFesta = document.getElementById("festa-planejamento");
const estadoFestas = document.getElementById("estado-festas");
const botaoEscolherFesta = document.getElementById("botao-escolher-festa");
const resumoFesta = document.getElementById("resumo-festa");
const formularioSugestao = document.getElementById("formulario-sugestao");
const botaoSugerir = document.getElementById("botao-sugerir");
const mensagemSugestao = document.getElementById("mensagem-sugestao");
const resultadoSugestao = document.getElementById("resultado-sugestao");
const botaoIrOrcamento = document.getElementById("botao-ir-orcamento");
const resumoOrcamentoFesta = document.getElementById("resumo-orcamento-festa");
const botaoAnalisarOrcamento = document.getElementById("botao-analisar-orcamento");
const mensagemOrcamento = document.getElementById("mensagem-orcamento");
const resultadoOrcamento = document.getElementById("resultado-orcamento");

let festasDisponiveis = [];
let festaSelecionada = null;

const nomesEtapas = {
    festa: "Festa",
    sugestao: "Sugestão",
    orcamento: "Orçamento",
    agenda: "Agenda",
    confirmacao: "Confirmação",
};

function mostrarEtapa(nomeEtapa, moverFoco = false) {
    const indice = linksEtapas.findIndex((link) => link.dataset.etapa === nomeEtapa);
    if (indice === -1) return;

    linksEtapas.forEach((link) => {
        if (link.dataset.etapa === nomeEtapa) link.setAttribute("aria-current", "step");
        else link.removeAttribute("aria-current");
    });
    paineisEtapas.forEach((painel) => {
        const painelAtual = painel.dataset.painel === nomeEtapa;
        painel.hidden = !painelAtual;
        if (painelAtual && moverFoco) painel.focus();
    });
    estadoEtapa.textContent = `Etapa ${indice + 1} de 5: ${nomesEtapas[nomeEtapa]}`;
}

function formatarMoeda(valor) {
    return Number(valor).toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

function criarTexto(tag, texto, classe = "") {
    const elemento = document.createElement(tag);
    elemento.textContent = texto;
    if (classe) elemento.className = classe;
    return elemento;
}

function exibirMensagemPlanejamento(elemento, texto, tipo = "") {
    elemento.textContent = texto;
    elemento.className = `mensagem-planejamento${tipo ? ` ${tipo}` : ""}`;
}

function renderizarPacote(itens) {
    resultadoSugestao.replaceChildren(criarTexto("h3", "Pacote sugerido", "titulo-resultado"));
    const lista = document.createElement("div");
    lista.className = "grade-resultado";
    itens.forEach((item) => {
        const cartao = document.createElement("article");
        cartao.className = "item-pacote";
        cartao.append(
            criarTexto("span", item.categoria.replaceAll("_", " "), "categoria-item"),
            criarTexto("h4", item.servico_nome),
            criarTexto("p", item.fornecedor_nome),
            criarTexto("strong", formatarMoeda(item.preco_referencia))
        );
        lista.appendChild(cartao);
    });
    resultadoSugestao.appendChild(lista);
}

function renderizarCategoriasSemCandidato(categorias) {
    resultadoSugestao.replaceChildren(
        criarTexto("h3", "Pacote não substituído", "titulo-resultado"),
        criarTexto("p", "Não encontramos serviços elegíveis para todas as categorias. O pacote anterior foi preservado.")
    );
    const lista = document.createElement("ul");
    categorias.forEach((categoria) => lista.appendChild(criarTexto("li", categoria.replaceAll("_", " "))));
    resultadoSugestao.appendChild(lista);
}

function criarIndicadorOrcamento(rotulo, valor) {
    const indicador = document.createElement("div");
    indicador.className = "indicador-orcamento";
    indicador.append(criarTexto("span", rotulo), criarTexto("strong", valor));
    return indicador;
}

function renderizarAnaliseOrcamento(analise) {
    const situacao = document.createElement("section");
    situacao.className = `situacao-orcamento ${analise.viavel ? "viavel" : "excedido"}`;
    situacao.append(
        criarTexto("h3", analise.viavel ? "Pacote dentro do orçamento" : "Pacote acima do orçamento"),
        criarTexto(
            "p",
            analise.viavel
                ? `Ainda restam ${formatarMoeda(analise.saldo)} no orçamento.`
                : `O pacote excede o orçamento em ${formatarMoeda(analise.excedente)}.`
        )
    );

    const indicadores = document.createElement("div");
    indicadores.className = "grade-orcamento";
    indicadores.append(
        criarIndicadorOrcamento("Orçamento", formatarMoeda(analise.orcamento)),
        criarIndicadorOrcamento("Total do pacote", formatarMoeda(analise.total)),
        criarIndicadorOrcamento("Percentual utilizado", `${Number(analise.percentual_utilizado).toLocaleString("pt-BR")} %`),
        criarIndicadorOrcamento("Custo por convidado", formatarMoeda(analise.custo_por_convidado))
    );
    resultadoOrcamento.replaceChildren(situacao, indicadores);
}

async function carregarFestas() {
    estadoFestas.textContent = "Carregando festas...";
    try {
        const festas = await requisicaoApi("/api/festas");
        festasDisponiveis = festas.filter((festa) => festa.status === "RASCUNHO");
        seletorFesta.replaceChildren();
        if (festasDisponiveis.length === 0) {
            seletorFesta.appendChild(new Option("Nenhuma festa em rascunho", ""));
            estadoFestas.textContent = "Cadastre uma festa em rascunho para começar.";
            return;
        }
        seletorFesta.appendChild(new Option("Selecione uma festa", ""));
        festasDisponiveis.forEach((festa) => {
            const texto = `${festa.nome} • ${festa.data} • ${festa.quantidade_convidados} convidados`;
            seletorFesta.appendChild(new Option(texto, String(festa.id)));
        });
        seletorFesta.disabled = false;
        estadoFestas.textContent = `${festasDisponiveis.length} festa(s) disponível(is).`;
    } catch (erro) {
        estadoFestas.textContent = `Erro: ${erro.message}`;
        estadoFestas.className = "mensagem-planejamento erro";
    }
}

seletorFesta.addEventListener("change", () => {
    botaoEscolherFesta.disabled = !seletorFesta.value;
});

botaoEscolherFesta.addEventListener("click", () => {
    festaSelecionada = festasDisponiveis.find((festa) => festa.id === Number(seletorFesta.value));
    if (!festaSelecionada) return;
    resumoFesta.textContent = `${festaSelecionada.nome} • ${festaSelecionada.data} • ${festaSelecionada.quantidade_convidados} convidados`;
    resumoOrcamentoFesta.textContent = resumoFesta.textContent;
    botaoSugerir.disabled = false;
    window.location.hash = "sugestao";
    mostrarEtapa("sugestao", true);
});

formularioSugestao.addEventListener("submit", async (evento) => {
    evento.preventDefault();
    if (!festaSelecionada) {
        exibirMensagemPlanejamento(mensagemSugestao, "Escolha uma festa antes de gerar a sugestão.", "erro");
        return;
    }
    const categorias = Array.from(formularioSugestao.querySelectorAll('input[name="categoria"]:checked')).map((campo) => campo.value);
    if (categorias.length === 0) {
        exibirMensagemPlanejamento(mensagemSugestao, "Selecione ao menos uma categoria.", "erro");
        return;
    }

    botaoSugerir.disabled = true;
    botaoSugerir.textContent = "Gerando sugestão...";
    exibirMensagemPlanejamento(mensagemSugestao, "Consultando serviços disponíveis...");
    resultadoSugestao.replaceChildren();
    try {
        const resultado = await requisicaoApi("/api/planejamentos/sugestao", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ festa_id: festaSelecionada.id, categorias }),
        });
        if (resultado.completo) {
            exibirMensagemPlanejamento(mensagemSugestao, "Pacote sugerido com sucesso.", "sucesso");
            renderizarPacote(resultado.itens);
            botaoIrOrcamento.disabled = false;
            botaoAnalisarOrcamento.disabled = false;
        } else {
            exibirMensagemPlanejamento(mensagemSugestao, "Existem categorias sem candidato.", "erro");
            renderizarCategoriasSemCandidato(resultado.categorias_sem_candidato);
            botaoIrOrcamento.disabled = true;
        }
    } catch (erro) {
        exibirMensagemPlanejamento(mensagemSugestao, `Erro: ${erro.message}`, "erro");
    } finally {
        botaoSugerir.disabled = false;
        botaoSugerir.textContent = "Gerar sugestão";
    }
});

botaoIrOrcamento.addEventListener("click", () => {
    window.location.hash = "orcamento";
    mostrarEtapa("orcamento", true);
});

botaoAnalisarOrcamento.addEventListener("click", async () => {
    if (!festaSelecionada) return;
    botaoAnalisarOrcamento.disabled = true;
    botaoAnalisarOrcamento.textContent = "Analisando...";
    exibirMensagemPlanejamento(mensagemOrcamento, "Calculando os valores do pacote...");
    resultadoOrcamento.replaceChildren();
    try {
        const analise = await requisicaoApi(`/api/planejamentos/${festaSelecionada.id}/orcamento`);
        renderizarAnaliseOrcamento(analise);
        exibirMensagemPlanejamento(
            mensagemOrcamento,
            analise.viavel ? "O pacote cabe no orçamento." : "O pacote ultrapassa o orçamento.",
            analise.viavel ? "sucesso" : "erro"
        );
    } catch (erro) {
        exibirMensagemPlanejamento(mensagemOrcamento, `Erro: ${erro.message}`, "erro");
    } finally {
        botaoAnalisarOrcamento.disabled = false;
        botaoAnalisarOrcamento.textContent = "Analisar orçamento";
    }
});

linksEtapas.forEach((link) => link.addEventListener("click", () => mostrarEtapa(link.dataset.etapa, true)));
window.addEventListener("hashchange", () => mostrarEtapa(window.location.hash.slice(1) || "festa"));
mostrarEtapa(window.location.hash.slice(1) || "festa");
carregarFestas();
