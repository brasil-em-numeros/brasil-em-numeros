import re
import math
import pandas as pd
import datetime
import itertools as it
import plotly.express as px
import plotly.graph_objects as go

from textwrap import wrap
from collections import ChainMap, OrderedDict
from .downloader import download
from more_itertools import partition

pd.set_option("mode.chained_assignment", None)


def formato_padrao(desp):

    if desp.empty:
        return desp
    cols = list(desp.columns)

    # -----------------------
    #  Renomeando as colunas
    # -----------------------

    anomes = {
        'Ano e mês do lançamento' : 'ano_mes'
    }

    nome = {
        c : re.sub(r'^Nome ', '', c) for c in cols if c.startswith('Nome ')
    }

    valor = {
        c : c.replace(
            'Valor', ''
        ).replace(
            'a Pagar ', ''
        ).replace(
            '(R$)', ''
        ).strip() for c in cols if c.startswith('Valor ')
    }

    novo_nome = ChainMap(anomes, nome, valor)
    return desp[list(cols)].rename(
        columns = novo_nome
    ).pipe(
        lambda df: df.melt(
            id_vars = [c for c in df.columns if c not in set(valor.values())],
            value_name = 'valor',
            var_name   = 'modalidade'
        )
    )


def despesas(transform = lambda x: x, *args, **kwargs):

    def url(mes, ano = 2020):
        return f'https://raw.githubusercontent.com/brasil-em-numeros/dados-publicos/master/portaltransparencia/despesas-execucao/graficos/{ano:04d}{mes:02d}.csv'

    meses = range(1, 13)
    anos  = range(2014, 2021)

    url_list = [
        url(mes, ano) for mes, ano in it.product(meses, anos)
    ]

    def trans(x, *args, **kwargs):
        return transform(
            formato_padrao(pd.read_csv(x)), *args, **kwargs
        )
    
    url_list = download(url_list, trans, *args, **kwargs)
    desp = filter(lambda df: not df.empty, url_list)
    # desp = pd.concat(desp, sort = False)

    return desp


date_dict = OrderedDict(
    jan = "jan",
    feb = "fev",
    mar = "mar",
    apr = "abr",
    may = "mai",
    jun = "jun",
    jul = "jul",
    aug = "ago",
    sep = "set",
    oct = "out",
    nov = "nov",
    dec = "dez",
    January   = "Janeiro",
    February  = "Fevereiro",
    March     = "Março",
    April     = "Abril",
    May       = "Maio",
    June      = "Junho",
    July      = 'Julho',
    August    = "Agosto",
    September = "Setembro",
    October   = "Outubro",
    November  = "Novembro",
    December  = "Dezembro"
)

# ----------------------------
#  Gráficos sobre as despesas
# ----------------------------

# 1 - heatmap por mês e ano


def heatmap_data(desp):

    if desp.empty:
        return desp

    return desp.query(
        "modalidade == 'Pago'"
    ).query(
        "valor != 0"
    ).assign(
        data = lambda df: pd.to_datetime(
            df['ano_mes'] + "/01", format = "%Y/%m/%d"
        )
    ).assign(
        mes = lambda df: df['data'].apply(lambda d: d.strftime("%b").lower()),
        ano = lambda df: df['data'].dt.year
    ).groupby(
        ['ano', 'mes'],
        as_index = False
    ).sum()


def heatmap_chart(data_heat):

    data_heat = data_heat.pivot(
        'ano', 'mes', 'valor'
    ).sort_index().fillna(0)

    def key(x):
        for i, k in enumerate(date_dict.keys()):
            if x == k:
                break
        
        return i

    data_heat = data_heat[sorted(data_heat.columns, key = key)]
    fig  = px.imshow(
        data_heat.to_numpy(),
        x = [date_dict.get(c, c).title() for c in data_heat.columns],
        y = [str(i) for i in data_heat.index],
        labels = dict(color = "Gastos pagos"),
        color_continuous_scale = "RdYlGn_r"
    )

    return fig


def funcao_data(desp):

    if desp.empty:
        return desp

    df = desp.query(
        "modalidade == 'Pago'"
    ).groupby(
        ['ano_mes', "Função"], as_index = False
    ).sum()

    df['data'] = df['ano_mes'] + "/01"
    df['data'] = pd.to_datetime(df['data'], format = '%Y/%m/%d')

    return df


def funcao_chart(data_funcao):

    fig = go.Figure()
    hover_template = "<b>%{text}</b><br>Gasto: %{y:$,.0f}"
    funs = sorted(data_funcao['Função'].unique())
    for fun in funs:
        
        plot_data = data_funcao.loc[
            data_funcao['Função'] == fun
        ].sort_values(['data'])
        x = plot_data['data']
        y = plot_data['valor']
        fig.add_trace(
            go.Scatter(
                x = x,
                y = y,
                mode = "lines+markers",
                name = fun,
                text = plot_data['Função'],
                line = {'shape' : 'spline'},
                hovertemplate = hover_template
            )
        )

    fig.update_layout(yaxis_title = "Valor Pago")
    fig.update_layout(title = "Gastos por categoria")
    return fig


def ministerios_data(desp):

    if desp.empty:
        return desp
    
    df = desp.groupby(
        ['ano_mes', 'Órgão Superior'], as_index = False
    ).sum()

    # ----------------------
    #  Top 10 ministérios
    # ----------------------

    top10 = df.drop(
        columns = ['Órgão Superior'],
        errors  = 'ignore'
    ).groupby(
        ['ano_mes'], as_index = False
    ).rank(method = "min", ascending = False)

    top10.columns = ['rank']
    df = pd.merge(
        df, top10,
        how = "left",
        left_index = True,
        right_index = True
    ).assign(
        ministerio = lambda x: [
            "Outros" if r > 10 else m for m, r in zip(
                x['Órgão Superior'],
                x['rank']
            )
        ]
    ).groupby(
        ['ano_mes', 'ministerio'],
        as_index = False
    ).sum().drop(
        columns = ['rank']
    ).assign(
        data = lambda x: x['ano_mes'].apply(
            lambda d: datetime.datetime.strptime(d + "/01", "%Y/%m/%d").strftime("%b/%Y")
        )
    )

    return df


def ministerios_chart(ministerios_data):

    df = ministerios_data.sort_values(['ano_mes'])

    # --------------------------
    #  Calcula tamanho do eixo
    # --------------------------

    x_max = max(df['valor'])
    zeros = int(math.log10(x_max))
    x_final = x_max / pow(10, zeros)
    if (x_final % 1) < 0.5:
        x_final = int(x_final) + 0.5
    else:
        x_final = int(x_final) + 1.0
    eixo_x = [0, x_final * pow(10, zeros)]

    # ----------------------
    #  Calcula cada quadro
    # ----------------------

    # --- Temos que filtrar por ano_mes para
    # --- o plotly ordernar os meses de forma
    # --- correta

    fig  = go.Figure()
    for (am, dt), grp in df.groupby(['ano_mes', 'data']):

        ministerios, outro = partition(
            lambda x: x == 'Outros', grp['ministerio']
        )

        ministerios = sorted(ministerios)
        grp.loc[:, 'ministerio'] = pd.Categorical(
            grp['ministerio'], it.chain(ministerios, outro)
        )
        
        grp = grp.sort_values(['ministerio'])
        fig.add_trace(
            go.Scatter(
                visible=False,
                name = dt,
                x = grp['valor'],
                y = grp['ministerio'].apply(
                    lambda s: "<br>".join(wrap(s, width = 30))
                ),
                mode = "markers"
            )
        )

    fig.data[0].visible = True

    # Create and add slider
    steps = []
    for i in range(len(fig.data)):
        step = dict(
            method = "update",
            args = [
                {"visible": [False] * len(fig.data)}
            ],  # layout attribute
            label = fig.data[i].name
        )
        step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
        steps.append(step)

    sliders = [
        dict(
            active = 0,
            currentvalue = {"prefix": "Data: "},
            pad = {"t": 50},
            steps = steps
        )
    ]

    fig.update_layout(
        sliders = sliders,
        title = "Top 10 ministérios com maior gasto no mês",
        # -- Usar o abaixo com dados reais
        xaxis = dict(range = eixo_x, autorange = False),
        yaxis = dict(autorange = "reversed")
    )

    fig.update_xaxes( # the y-axis is in dollars
        showgrid=False
    )

    return fig
