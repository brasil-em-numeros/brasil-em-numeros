from flask import Blueprint, render_template
from flask import current_app as app


about_bp = Blueprint(
    name = "about_bp",
    import_name = __name__,
    template_folder = "templates",
    static_folder = 'assets'
)


@about_bp.route("/about")
def about_page():
    return render_template(
        "about.html", title = 'Brasil em Números'
    )
