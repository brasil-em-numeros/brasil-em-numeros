from flask import Blueprint, render_template, request, make_response
from flask import session, jsonify
from flask import current_app as app
import plotly.express as px
import json


pdt_bp = Blueprint(
    name = "pdt_bp",
    import_name = __name__,
    template_folder = "templates",
    static_folder = 'assets'
)


def json_headers():
    return {'Content-Type' : 'application/json'}


@pdt_bp.before_app_first_request
def set_defaults():
    session['year'] = 2007


def gapminder(year = 2007):

    df = px.data.gapminder()
    df = df.loc[df['year'] == year]
    fig = px.scatter(
        df,
        x = "gdpPercap",
        y = "lifeExp",
        size  = "pop",
        color = "continent",
        hover_name = "country",
        log_x = True,
        size_max = 60
    )

    return json.loads(fig.to_json()).get('data')


@pdt_bp.route("/pdt", methods = ['GET', 'POST'])
def pdt_page():

    if request.method == 'POST':
        year = request.get_json()
        year = int(year)
        session['year'] = year
        print(session['year'])
        return make_response(
            'Updating data succeeded!', 200, json_headers()
        )

    return render_template(
        "pdt.html",
        title = 'Portal da transparência'#,
        # plot_data = json.dumps(gapminder(g.year))
    )


@pdt_bp.route("/pdt_data")
def pdt_data():

    data = gapminder(session['year'])
    # data.insert(0, g.year)
    print(session.get('year'))
    return make_response(jsonify(data), 200, json_headers())
