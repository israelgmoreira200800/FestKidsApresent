const linksEtapas = Array.from(document.querySelectorAll("[data-etapa]"));
const paineisEtapas = Array.from(document.querySelectorAll("[data-painel]"));
const estadoEtapa = document.getElementById("estado-etapa");

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
        if (link.dataset.etapa === nomeEtapa) {
            link.setAttribute("aria-current", "step");
        } else {
            link.removeAttribute("aria-current");
        }
    });

    paineisEtapas.forEach((painel) => {
        const painelAtual = painel.dataset.painel === nomeEtapa;
        painel.hidden = !painelAtual;
        if (painelAtual && moverFoco) painel.focus();
    });

    estadoEtapa.textContent = `Etapa ${indice + 1} de 5: ${nomesEtapas[nomeEtapa]}`;
}

linksEtapas.forEach((link) => {
    link.addEventListener("click", () => {
        mostrarEtapa(link.dataset.etapa, true);
    });
});

window.addEventListener("hashchange", () => {
    mostrarEtapa(window.location.hash.slice(1) || "festa");
});

mostrarEtapa(window.location.hash.slice(1) || "festa");
