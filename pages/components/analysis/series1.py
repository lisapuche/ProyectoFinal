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
df_date1 = df.groupby('fecha_hecho')['cantidad'].sum().reset_index()

df_date2 = df.groupby(df.fecha_hecho.dt.year)['cantidad'].sum().reset_index()
df_date2 = df_date2.rename({'fecha_hecho':'year'}, axis=1)
fig = make_subplots(rows=3, cols=1, vertical_spacing=0.1, subplot_titles=(
    'Timeline de casos diarios',
    'Total de casos agrupados por año',
    'Distribución de casos diarios desde 2019 hasta 2022'
))

fig.add_trace(
    go.Scatter(x=df_date1['fecha_hecho'], y=df_date1['cantidad'], mode='lines+markers', name='Casos Diarios', line=dict(color='blue')),
    row=1, col=1
)

fig.add_trace(
    go.Bar(x=df_date2['year'], y=df_date2['cantidad'], name='Casos por Año', marker=dict(color='green')),
    row=2, col=1
)

df_date1_filtered = df_date1[df_date1['fecha_hecho'] > '2019-01-01']
fig.add_trace(
    go.Scatter(x=df_date1_filtered['fecha_hecho'], y=df_date1_filtered['cantidad'], mode='lines+markers', name='Casos desde 2019', line=dict(color='red')),
    row=3, col=1
)

fig.update_xaxes(title_text="Fecha", row=1, col=1)
fig.update_yaxes(title_text="Casos", row=1, col=1)
fig.update_xaxes(title_text="Años", row=2, col=1)
fig.update_yaxes(title_text="Casos", row=2, col=1)
fig.update_xaxes(title_text="Fecha", row=3, col=1)
fig.update_yaxes(title_text="Casos", row=3, col=1)

fig.update_layout(height=800, showlegend=False)

def series1_layout():
    layout = html.Div(
        [
            dcc.Loading(children=[dcc.Graph(figure=fig)]),
        ]
    )
    return layout


def series1_content():
    return html.Div(
        [
            html.Div([html.H3("👁‍🗨 Observaciones")]),
            html.Div(
                [
                    html.P(
                        "Frecuencia de casos cada día a lo largo de varios años. Hay picos evidentes a través del tiempo, lo que podría indicar eventos o circunstancias específicas que causaron aumentos temporales en el número de casos."
                    )
                ]
            ),
        ]
    )


@my_app.callback(
    Output("series1", "data"),
    Input("series1_bt", "n_clicks"),
    prevent_initial_call=True,
)

def series1_info():
    return (series1_content(), series1_layout())


@my_app.callback(
    Output("series1", "is_open"),
    [Input("series1_bt", "n_clicks")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open