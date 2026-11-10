from backend.routes.cliente_routes import cliente_blueprint
from backend.routes.health_routes import health_blueprint


def registrar_rotas(app):
    app.register_blueprint(health_blueprint)
    app.register_blueprint(cliente_blueprint)
