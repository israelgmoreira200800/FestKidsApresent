from backend.extensions import db


class PlanejamentoItem(db.Model):
    __tablename__ = "planejamento_itens"

    id = db.Column(db.Integer, primary_key=True)
    festa_id = db.Column(
        db.Integer,
        db.ForeignKey("festas.id"),
        nullable=False,
    )
    servico_id = db.Column(
        db.Integer,
        db.ForeignKey("servicos.id"),
        nullable=False,
    )
    preco_referencia = db.Column(db.Numeric(12, 2), nullable=False)
    criado_em = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
    )

    __table_args__ = (
        db.UniqueConstraint(
            "festa_id",
            "servico_id",
            name="uq_planejamento_item_festa_servico",
        ),
    )

    def para_dict(self):
        return {
            "id": self.id,
            "festa_id": self.festa_id,
            "servico_id": self.servico_id,
            "preco_referencia": format(self.preco_referencia, ".2f"),
            "criado_em": self.criado_em.isoformat(),
        }
