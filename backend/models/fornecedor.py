from backend.extensions import db


class Fornecedor(db.Model):
    __tablename__ = "fornecedores"

    id = db.Column(db.Integer, primary_key=True)
    nome_comercial = db.Column(db.String(120), nullable=False)
    email = db.Column(
        db.String(255),
        nullable=False,
        unique=True,
    )
    telefone = db.Column(db.String(20), nullable=False)
    disponivel = db.Column(db.Boolean, nullable=False, default=True)
    criado_em = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
    )

    def para_dict(self):
        return {
            "id": self.id,
            "nome_comercial": self.nome_comercial,
            "email": self.email,
            "telefone": self.telefone,
            "disponivel": self.disponivel,
            "criado_em": self.criado_em.isoformat(),
        }
