from .app import app
from flask import render_template
from .layouts import update_template, route_feeder_pages


def run_app(app, **kws):

    update_template()
    route_feeder_pages(app = app)

    @app.route("/")
    @app.route("/home")
    def index():
        return render_template("home.html")

    @app.route("/about")
    def about():
        return render_template("about.html")

    app.run(**kws)


if __name__ == "__main__":
    run_app(app, debug = True)
