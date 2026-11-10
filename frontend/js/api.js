const URL_BASE_API = "http://127.0.0.1:5000";

async function requisicaoApi(caminho, opcoes = {}) {
    const resposta = await fetch(`${URL_BASE_API}${caminho}`, opcoes);
    const dados = await resposta.json();
    if (!resposta.ok) {
        throw new Error(dados.erro ? dados.erro.mensagem : "Não foi possível concluir a operação.");
    }
    return dados;
}

function mostrarMensagem(elemento, texto, tipo) {
    elemento.textContent = texto;
    elemento.className = `mensagem ${tipo}`;
}

function criarCartaoRegistro(titulo, detalhes, aoEditar, aoExcluir) {
    const cartao = document.createElement("article");
    cartao.className = "registro";
    const conteudo = document.createElement("div");
    const nome = document.createElement("h3");
    nome.textContent = titulo;
    conteudo.appendChild(nome);
    detalhes.forEach(function (detalhe) {
        const texto = document.createElement("p");
        texto.textContent = detalhe;
        conteudo.appendChild(texto);
    });
    const acoes = document.createElement("div");
    acoes.className = "acoes-registro";
    const editar = document.createElement("button");
    editar.type = "button";
    editar.className = "botao-acao";
    editar.textContent = "Editar";
    editar.addEventListener("click", aoEditar);
    const excluir = document.createElement("button");
    excluir.type = "button";
    excluir.className = "botao-acao perigo";
    excluir.textContent = "Excluir";
    excluir.addEventListener("click", aoExcluir);
    acoes.append(editar, excluir);
    cartao.append(conteudo, acoes);
    return cartao;
}
