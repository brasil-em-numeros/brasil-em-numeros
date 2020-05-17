from flask import Flask
from .layouts import update_template


def create_app():
    """Create Flask application."""

    app = Flask(
        __name__,
        static_folder = "assets",
        instance_relative_config = False
    )
    update_template()
    with app.app_context():
        
        # ------------
        #  Provedores
        # ------------
        
        app.secret_key = '12345'
        from .home import home
        from .about import about
        from .provedores.pdt import pdt
        from .provedores.ibge import ibge

        # -------------------
        # Register Blueprints
        # -------------------

        app.register_blueprint(home.home_bp)
        app.register_blueprint(about.about_bp)
        app.register_blueprint(pdt.pdt_bp)
        app.register_blueprint(ibge.ibge_bp)

        return app
