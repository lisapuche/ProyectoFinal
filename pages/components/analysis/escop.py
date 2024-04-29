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
dfsco = df.query('armas_medios == "ARMA DE FUEGO"')
dfdsco = pd.pivot_table(dfsco, index = 'departamento', values = 'cantidad', columns = None, aggfunc='count').reset_index()
dfdsco['departamento'].replace({'ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA':'SAN ANDRES'}, inplace=True)

fig = px.bar(dfdsco, x='cantidad', y='departamento', text_auto='.2s', 
            title="Número de informes de violencia familiar con arma de fuego por departamento", 
            labels={'departamento':'Departamento', 'cantidad':'Casos'}, orientation='h')

fig.update_traces(textfont_size=12, textangle=0, textposition="outside",cliponaxis=False)
fig.update_layout(width=900, height=800)

def dep_layout():
    layout = html.Div(
        dcc.Loading(children=[dcc.Graph(figure=fig)]),
        style={'width': '100%', 'display': 'flex', 'justify-content': 'center'}
    )
    return layout


def dep_content():
    return html.Div(
        [
            html.Div([html.H3("👁‍🗨 Observaciones")]),
            html.Div(
                [
                    html.P(
                        "Cantidad de casos de Violencia reportados con Arma de Fuego por departamento."
                    )
                ]
            ),
        ]
    )


@my_app.callback(
    Output("dep", "data"),
    Input("dep_bt", "n_clicks"),
    prevent_initial_call=True,
)

def dep_info():
    return (dep_content(), dep_layout())


@my_app.callback(
    Output("dep", "is_open"),
    [Input("dep_bt", "n_clicks")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open