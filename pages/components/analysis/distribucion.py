# dash imports
import plotly.express as px
from dash import html
from dash import Input
from dash import Output
from dash import dcc
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from dash import State
from scipy.stats import probplot
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# file imports
from maindash import my_app
from maindash import df
from Utils.file_operation import read_file_as_str

#Grafico
num_columns = len(df.columns)
num_rows = num_columns // 2 if num_columns % 2 == 0 else (num_columns // 2) + 1

fig = make_subplots(rows=num_rows, cols=2, subplot_titles=df.columns)

for i, column in enumerate(df.columns):
    fig.add_trace(
        go.Histogram(x=df[column], nbinsx=50, name=column),
        row=(i // 2) + 1,
        col=(i % 2) + 1
    )
fig.update_layout(
    width=1000,
    height=500 * num_rows,
    title_text="Histograms of DataFrame Columns"
)


def distribucion_layout():
    layout = html.Div(
        [
            dcc.Loading(children=[dcc.Graph(figure=fig)]),
        ]
    )
    return layout


def distribucion_content():
    return html.Div(
        [
            html.Div([html.H3("👁‍🗨 Observaciones")]),
            html.Div(
                [
                    html.P(
                        "Distribución de frecuencia para cada una de las variables"
                    )
                ]
            ),
        ]
    )


@my_app.callback(
    Output("Distribución de Datos_Histogramas", "data"),
    Input("Distribución de Datos_Histogramas_bt", "n_clicks"),
    prevent_initial_call=True,
)

def distribucion_info():
    return (distribucion_content(), distribucion_layout())


@my_app.callback(
    Output("Distribución de Datos_Histogramas", "is_open"),
    [Input("Distribución de Datos_Histogramas_bt", "n_clicks")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open