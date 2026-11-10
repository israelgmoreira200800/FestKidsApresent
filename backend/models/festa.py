from backend.extensions import db


class Festa(db.Model):
    __tablename__ = "festas"

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id"),
        nullable=False,
    )
    nome = db.Column(db.String(120), nullable=False)
    data = db.Column(db.Date, nullable=False)
    local = db.Column(db.String(180), nullable=False)
    quantidade_convidados = db.Column(db.Integer, nullable=False)
    orcamento = db.Column(db.Numeric(12, 2), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="RASCUNHO")
    criado_em = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
    )

    def para_dict(self):
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "nome": self.nome,
            "data": self.data.isoformat(),
            "local": self.local,
            "quantidade_convidados": self.quantidade_convidados,
            "orcamento": format(self.orcamento, ".2f"),
            "status": self.status,
            "criado_em": self.criado_em.isoformat(),
        }
