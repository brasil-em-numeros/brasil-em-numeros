from flask import Blueprint, render_template, request, make_response
from flask import session, jsonify
from flask import current_app as app
import plotly.express as px
import json

from . import despesas_publicas as desp


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

    dados = desp.despesas()
    gf = dict(
        fun  = desp.funcao_por_ano(dados),
        min  = desp.gastos_por_ministerio(dados),
        heat = desp.heatmap(dados)
    )

    gf = {
        k : v.to_json() for k, v in gf.items()
    }

    return gf


graficos = grafico_despesas()


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

    # graficos = grafico_despesas()
    return render_template(
        "pdt.html",
        title = 'Portal da transparência',
        funcao = graficos['fun'],
        ministerio  = graficos['min'],
        heat = graficos['heat']
    )
