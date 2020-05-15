from flask import Blueprint, render_template
from flask import current_app as app


ibge_bp = Blueprint(
    "ibge_bp",
    import_name = __name__,
    template_folder = 'templates',
    static_folder = 'assets'
)

@ibge_bp.route("/ibge")
def ibge_page():
    return render_template(
        "ibge.html", title = "IBGE"
    )