from backend.routes.health_routes import health_blueprint


def registrar_rotas(app):
    app.register_blueprint(health_blueprint)
