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
gun_table = pd.pivot_table(df, index = 'armas_medios', values = 'cantidad', columns = None, aggfunc='count',sort=True).reset_index()
gun_table
colors = ['skyblue', 'green', 'red', 'purple', 'orange']
gun_graph = px.bar(gun_table, x='armas_medios', y='cantidad', text_auto='.2s', title='Tipo de arma usada',color='armas_medios', color_discrete_sequence=colors )
gun_graph.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
gun_graph.update_xaxes(tickvals=[0, 1, 2, 3, 4], ticktext=['ARMA BLANCA', 'ARMA DE FUEGO', 'ESCOPOLAMINA ', 'SIN EMPLEO DE ARMAS ','Unknown'])

def arma_layout():
    layout = html.Div(
        [
            dcc.Loading(children=[dcc.Graph(figure=gun_graph)]),
        ]
    )
    return layout


def arma_content():
    return html.Div(
        [
            html.Div([html.H3("👁‍🗨 Observaciones")]),
            html.Div(
                [
                    html.P(
                        "ARMA BLANCA es la categoría más común con 320 mil casos reportados."
                    )
                ]
            ),
        ]
    )


@my_app.callback(
    Output("barras", "data"),
    Input("barras_bt", "n_clicks"),
    prevent_initial_call=True,
)

def arma_info():
    return (arma_content(), arma_layout())


@my_app.callback(
    Output("barras", "is_open"),
    [Input("barras_bt", "n_clicks")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open