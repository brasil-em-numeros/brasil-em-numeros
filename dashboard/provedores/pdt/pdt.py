from flask import Blueprint, render_template, request, make_response
from flask import session, jsonify
from flask import current_app as app
import json
import pandas as pd

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


def grafico_despesas():

    print("")
    print("Baixando dados...")
    gf = (
        (
            desp.funcao_data(g),
            desp.ministerios_data(g),
            desp.heatmap_data(g)
        ) for g in desp.despesas()
    )

    gf = zip(*gf)
    gf = (
        chart(pd.concat(data, sort = False)) for chart, data in zip(
            [desp.funcao_chart, desp.ministerios_chart, desp.heatmap_chart],
            gf
        )
    )

    print("Executando gráficos...")
    graficos = dict()
    for k, v in zip(['fun', 'min', 'heat'], gf):
        graficos[k] = v.to_json()
    
    return graficos


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
        funcao = app.charts_cache.get('fun'),
        ministerio = app.charts_cache.get('min'),
        heat = app.charts_cache.get('heat')
    )
