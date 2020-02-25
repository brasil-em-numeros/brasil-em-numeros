import pandas as pd
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px

# ===================
#    Extract data
# ===================

data_path = os.path.abspath(os.path.dirname(__file__))

data = pd.read_csv(os.path.join(data_path, "data.csv"))
data = pd.melt(data, id_vars = 'orgao', value_name = "value", var_name = "type")

fig = px.bar(
    data, x = "orgao", y = "value", color = "type", hover_data = ["value"],
    barmode='group'
)

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(
    __name__, 
    external_stylesheets = external_stylesheets
)

app.layout = html.Div(
    children=[
        html.H1(children="Hello Dashboard"),
        html.Div(
            children = """
            Dash: A web application framework for Python.
            """
        ),
        dcc.Graph(
            id = "example-graph",
            figure = fig
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True, port = "8050")
