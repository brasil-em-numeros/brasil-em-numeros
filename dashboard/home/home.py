from flask import Blueprint, render_template
from flask import current_app as app


home_bp = Blueprint(
    name = "home_bp",
    import_name = __name__,
    template_folder = "templates",
    static_folder = 'assets'
)


@home_bp.route("/home")
@home_bp.route("/")
def home_page():
    return render_template(
        "home.html", title = 'Bem-vindo ao Brasil em Números'
    )
