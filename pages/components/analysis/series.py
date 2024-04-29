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
df['day'] = df['fecha_hecho'].dt.day_name()
df['month'] = df['fecha_hecho'].dt.month_name()
new_order_month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
new_order_day = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

df_day = df.groupby('day')['cantidad'].sum().reindex(new_order_day, axis=0).reset_index()
df_month = df.groupby('month')['cantidad'].sum().reindex(new_order_month, axis=0).reset_index()

fig = make_subplots(rows=2, cols=1, subplot_titles=('Casos por mes', 'Casos por día de la semana'))

for i, (month, cases) in enumerate(zip(df_month['month'], df_month['cantidad'])):
    fig.add_trace(
        go.Bar(x=[month], y=[cases], text=[str(cases)], textposition='auto'),
        row=1, col=1
    )
    
for i, (day, cases) in enumerate(zip(df_day['day'], df_day['cantidad'])):
    fig.add_trace(
        go.Bar(x=[day], y=[cases], text=[str(cases)], textposition='auto'),
        row=2, col=1
    )

fig.update_xaxes(title_text="Meses", row=1, col=1, tickangle=25)
fig.update_yaxes(title_text="Casos", row=1, col=1)

fig.update_xaxes(title_text="Días de la semana", row=2, col=1, tickangle=25)
fig.update_yaxes(title_text="Casos", row=2, col=1)

fig.update_layout(height=800, showlegend=False)

def series_layout():
    layout = html.Div(
        [
            dcc.Loading(children=[dcc.Graph(figure=fig)]),
        ]
    )
    return layout


def series_content():
    return html.Div(
        [
            html.Div([html.H3("👁‍🗨 Observaciones")]),
            html.Div(
                [
                    html.P(
                        "Distribución de casos por mes, con el mayor número de casos reportados en febrero y una tendencia general decreciente hacia el final del año, con diciembre como el mes con menos casos."
                    )
                ]
            ),
        ]
    )


@my_app.callback(
    Output("series", "data"),
    Input("series_bt", "n_clicks"),
    prevent_initial_call=True,
)

def series_info():
    return (series_content(), series_layout())


@my_app.callback(
    Output("series", "is_open"),
    [Input("series_bt", "n_clicks")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open