from flask import Blueprint, render_template, request, make_response
from flask import session, jsonify
from flask import current_app as app
import plotly.express as px
import json


pdt_bp = Blueprint(
    name = "pdt_bp",
    import_name = __name__,
    template_folder = "templates",
    static_folder = 'assets',
    url_prefix = '/pdt'
)


def json_headers():
    return {'Content-Type' : 'application/json'}


@pdt_bp.before_app_first_request
def set_defaults():
    session['year'] = 2007
    session['modalidade'] = 'Pago'


def grafico_despesas():

    gf = dict(
        fun = funcao_por_ano(despesas()),
        min = gastos_por_ministerio(despesas())
    )

    gf = {
        k : v.to_json() for k, v in gf.items()
    }

    return gf


@pdt_bp.route("/pdt", methods = ['GET', 'POST'])
def pdt_page():

    if request.method == 'POST':
        js = request.get_json()
        
        for key, val in js.items():
            print("{} : {}".format(key, val))
            session[key] = val
        
        return make_response(
            'Updating data succeeded!', 200, json_headers()
        )

    graficos = grafico_despesas()
    return render_template(
        "pdt.html",
        title = 'Portal da transparência',
        funcao = graficos['fun'],
        ministerio  = graficos['min']
    )
