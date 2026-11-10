from backend.extensions import db


class Servico(db.Model):
    __tablename__ = "servicos"

    id = db.Column(db.Integer, primary_key=True)
    fornecedor_id = db.Column(
        db.Integer,
        db.ForeignKey("fornecedores.id"),
        nullable=False,
    )
    nome = db.Column(db.String(120), nullable=False)
    descricao = db.Column(db.Text)
    categoria = db.Column(db.String(40), nullable=False)
    preco_base = db.Column(db.Numeric(12, 2), nullable=False)
    capacidade_convidados = db.Column(db.Integer, nullable=False)
    disponivel = db.Column(db.Boolean, nullable=False, default=True)
    criado_em = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
    )

    def para_dict(self):
        return {
            "id": self.id,
            "fornecedor_id": self.fornecedor_id,
            "nome": self.nome,
            "descricao": self.descricao,
            "categoria": self.categoria,
            "preco_base": format(self.preco_base, ".2f"),
            "capacidade_convidados": self.capacidade_convidados,
            "disponivel": self.disponivel,
            "criado_em": self.criado_em.isoformat(),
        }
