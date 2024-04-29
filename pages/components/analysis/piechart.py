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
fig = px.pie(
    df, 
    names='genero', 
    values='cantidad', 
    title='Víctimas por Género'
)

fig.update_traces(textinfo='percent+label', textfont_size=14)

def pie_layout():
    layout = html.Div(
        [
            dcc.Loading(children=[dcc.Graph(figure=fig)]),
        ]
    )
    return layout


def pie_content():
    return html.Div(
        [
            html.Div([html.H3("👁‍🗨 Observaciones")]),
            html.Div(
                [
                    html.P(
                        "El género FEMENINO representando el '77.7%' y la categoría MASCULINO el '22.3%' de los casos reportados."
                    )
                ]
            ),
        ]
    )


@my_app.callback(
    Output("pie", "data"),
    Input("pie_bt", "n_clicks"),
    prevent_initial_call=True,
)

def pie_info():
    return (pie_content(), pie_layout())


@my_app.callback(
    Output("pie", "is_open"),
    [Input("pie_bt", "n_clicks")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open