from flask import Blueprint, render_template
from flask import current_app as app


pdt_bp = Blueprint(
    name = "pdt_bp",
    import_name = __name__,
    template_folder = "templates",
    static_folder = 'assets',
    url_prefix = '/pdt'
)


@pdt_bp.route("/pdt")
def pdt_page():
    return render_template(
        "pdt.html", title = 'Portal da transparência'
    )
