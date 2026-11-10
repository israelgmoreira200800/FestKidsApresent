class ErroAplicacao(Exception):
    codigo = "erro_aplicacao"
    status_http = 400

    def __init__(self, mensagem):
        super().__init__(mensagem)
        self.mensagem = mensagem


class ErroValidacao(ErroAplicacao):
    codigo = "validacao"
    status_http = 400


class RecursoNaoEncontrado(ErroAplicacao):
    codigo = "nao_encontrado"
    status_http = 404


class ErroConflito(ErroAplicacao):
    codigo = "conflito"
    status_http = 409
