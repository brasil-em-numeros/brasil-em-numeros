import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

from dash.dependencies import Input, Output
from .app import app

from .data import fake_data
from .html_helpers import *

df = fake_data()


def home_layout():

    page = html.H1(
        "Brasil em números", className = "mt-4"
    )

    inicio = data_source_element('Início', 'index.html')
    header = page_header([inicio])
    sidebar = main_sidebar([
        data_source_element(
            'Portal da transparência',
            "pdt.html",
            "fas fa-comments-dollar"
        ),
        data_source_element(
            'IBGE',
            "ibge.html",
            "fas fa-globe-americas"
        )
    ])

    main_ = main(page)

    content = [
        header,
        html.Div(
            id = "layoutSidenav",
            children = [
                sidebar,
                main_
            ]
        )
    ]
    return html.Div(content)


def slider():

    rng = sorted(df['ano'].unique())
    date_range = dcc.RangeSlider(
        id = "slider-ano",
        min = rng[0],
        max = rng[-1],
        step = 1,
        value = [rng[0], rng[-1]],
        marks = {r : str(r) for r in rng}
    )

    return html.Div(
        className = "container",
        children = [
            html.Div(
                html.P("Use o slider abaixo para selecionar os anos"),
                className = "row"
            ),
            date_range
        ]
    )


def dropdown():

    estados = df[[
        'nome_uf', 'nome_uf_sigla'
    ]].drop_duplicates()

    estados = [
        {'label' : row['nome_uf'], 'value' : row['nome_uf_sigla']} for _, row in estados.iterrows()
    ]

    return dcc.Dropdown(
        id = 'estados',
        options = estados,
        value   = [e['value'] for e in estados],
        multi   = True
    )


@app.callback(
    Output('chart', 'figure'),
    [
        Input('slider-ano', 'value'),
        Input('estados', 'value')
    ]
)
def update_chart(anos, estados):
    def chart(data, anos = None):

        if anos is not None:

            amin = anos[0]
            amax = anos[1]
            data = data.loc[
                (data['ano'] <= amax) &
                (data['ano'] >= amin)
            ]

        if estados:
            data = data.loc[
                data['nome_uf_sigla'].isin(estados)
            ]

        fig = px.bar(data, x="ano", y="valor", color="nome_uf", barmode="group")
        return fig

    return chart(df, anos)
