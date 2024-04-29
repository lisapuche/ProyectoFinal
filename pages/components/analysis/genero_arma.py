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
dfsex = pd.pivot_table(df, index = ('genero', 'armas_medios'), values = 'cantidad', columns = None, aggfunc='count', sort=True).reset_index()
dfsex

fig_sex = px.bar(dfsex, x='genero', y='cantidad', color='armas_medios', barmode='group', text_auto='.2s', 
                title="Género de las víctimas y el número de casos que involucran cada tipo de arma", 
                labels={'Cantidad':'Casos', 'genero':'Género y tipo de arma'}, height=400)

fig_sex.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

def barsex_layout():
    layout = html.Div(
        [
            dcc.Loading(children=[dcc.Graph(figure=fig_sex)]),
        ]
    )
    return layout


def barsex_content():
    return html.Div(
        [
            html.Div([html.H3("👁‍🗨 Observaciones")]),
            html.Div(
                [
                    html.P(
                        "El número más elevado de casos para las víctimas femeninas (250k) se da en situaciones donde se emplea ARMA BLANCA."
                    )
                ]
            ),
        ]
    )


@my_app.callback(
    Output("barsex", "data"),
    Input("barsex_bt", "n_clicks"),
    prevent_initial_call=True,
)

def barsex_info():
    return (barsex_content(), barsex_layout())


@my_app.callback(
    Output("barsex", "is_open"),
    [Input("barsex_bt", "n_clicks")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open