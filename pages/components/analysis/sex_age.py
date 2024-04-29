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
dfsex_age = pd.pivot_table(df, index = ('genero', 'grupo_etario'), values = 'cantidad', columns = None, aggfunc='count', sort=True).reset_index()
dfsex_age
fig_sex_age = px.bar(dfsex_age, x='genero', y='cantidad', color='grupo_etario', barmode='group', text_auto='.2s', 
                    title="Género de las victimas y número de casos según la Edad", 
                    labels={'cantidad':'Casos', 'genero':'Género y Edad'}, height=400)

fig_sex_age.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

def sexage_layout():
    layout = html.Div(
        [
            dcc.Loading(children=[dcc.Graph(figure=fig_sex_age)]),
        ]
    )
    return layout


def sexage_content():
    return html.Div(
        [
            html.Div([html.H3("👁‍🗨 Observaciones")]),
            html.Div(
                [
                    html.P(
                        "Para el género femenino, hay un número significativamente mayor de casos en la categoría de adultos (390k). En cuanto al género masculino, también predominan los casos en adultos (110k), pero la diferencia entre adolescentes (11k) y menores (18k) es menos pronunciada."
                    )
                ]
            ),
        ]
    )


@my_app.callback(
    Output("barsexage", "data"),
    Input("barsexage_bt", "n_clicks"),
    prevent_initial_call=True,
)

def sexage_info():
    return (sexage_content(), sexage_layout())


@my_app.callback(
    Output("barsexage", "is_open"),
    [Input("barsexage_bt", "n_clicks")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open