from backend.extensions import db


class Cliente(db.Model):
    __tablename__ = "clientes"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(
        db.String(255),
        nullable=False,
        unique=True,
    )
    telefone = db.Column(db.String(20), nullable=False)
    criado_em = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
    )

    def para_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "telefone": self.telefone,
            "criado_em": self.criado_em.isoformat(),
        }
