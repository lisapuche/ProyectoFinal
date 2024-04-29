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
from phik import phik_matrix
from scipy.stats import probplot
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# file imports
from maindash import my_app
from maindash import df
from Utils.file_operation import read_file_as_str

#Grafico
df_factorize = df.apply(lambda x : pd.factorize(x)[0]) 
df_corr = df_factorize.phik_matrix(interval_cols=list(df.columns)).copy()

fig = px.imshow(df_corr.values,
                labels=dict(x="", y="", color="Correlación"),
                x=df_corr.columns,
                y=df_corr.columns,
                color_continuous_scale='RdBu')

fig.update_layout(title="Mapa de calor de correlación",
                  width=800,
                  height=600)

def corr_layout():
    layout = html.Div(
        [
            dcc.Loading(children=[dcc.Graph(figure=fig)]),
        ]
    )
    return layout


def corr_content():
    return html.Div(
        [
            html.Div([html.H3("👁‍🗨 Observaciones")]),
            html.Div(
                [
                    html.P(
                        "La relación más fuerte se ve entre la variable Armas_medios y Genero."
                    )
                ]
            ),
        ]
    )


@my_app.callback(
    Output("corr", "data"),
    Input("corr_bt", "n_clicks"),
    prevent_initial_call=True,
)

def corr_info():
    return (corr_content(), corr_layout())


@my_app.callback(
    Output("corr", "is_open"),
    [Input("corr_bt", "n_clicks")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open