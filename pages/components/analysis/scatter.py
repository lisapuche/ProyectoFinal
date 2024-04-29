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
def nueva_region(departamento):
    if departamento in ['AMAZONAS', 'CAQUETA', 'GUAINIA', 'VAUPES', 'GUAVIARE', 'PUTUMAYO']:
        return 'Amazónica'
    elif departamento in ['ANTIOQUIA', 'BOYACA', 'CALDAS', 'CUNDINAMARCA', 'SANTAFE DE BOGOTA D.C', 'HUILA', 'NORTE DE SANTANDER', 'QUINDIO', 'RISARALDA', 'SANTANDER', 'TOLIMA']:
        return 'Andina'
    elif departamento in ['VALLE DEL CAUCA', 'CHOCO', 'CAUCA', 'NARIÑO']:
        return 'Pacífica'
    elif departamento in ['ATLANTICO', 'BOLIVAR', 'CESAR', 'CORDOBA', 'LA GUAJIRA', 'MAGDALENA', 'SUCRE', 'ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA']:
        return 'Caribe'
    elif departamento in ['ARAUCA', 'CASANARE', 'META', 'VICHADA']:
        return 'Orinoquía'
    else:
        return 'Desconocido' 


df['region'] = df['departamento'].apply(nueva_region)

df['fecha_hecho'] = pd.to_datetime(df['fecha_hecho'])
df['mes'] = df['fecha_hecho'].dt.month
df['año'] = df['fecha_hecho'].dt.year

#Agrupar los datos por mes, año y región, sumando la cantidad de casos
df_suma = df.groupby(['año', 'mes', 'region'])['cantidad'].sum().reset_index()

fig = px.scatter(df_suma, x='mes', y='cantidad', color='region', hover_data=['region'], title='Evolución de la violencia en Colombia',
                 labels={'mes': 'Mes', 'cantidad': 'Cantidad de casos', 'region': 'Región'}, animation_frame='año')

#Slider de año
fig.update_layout(xaxis=dict(type='category'), yaxis=dict(range=[0, df_suma['cantidad'].max() * 1]))
fig.update_traces(marker=dict(size=10, opacity=0.8))


def scatter_layout():
    layout = html.Div(
        [
            dcc.Loading(children=[dcc.Graph(figure=fig)]),
        ]
    )
    return layout


def scatter_content():
    return html.Div(
        [
            html.Div([html.H3("👁‍🗨 Observaciones")]),
            html.Div(
                [
                    html.P(
                        "La región Andina a través de los años se ha catalogado como una de las zonas del país con más registros de violencia doméstica."
                    )
                ]
            ),
        ]
    )


@my_app.callback(
    Output("scatter", "data"),
    Input("scatter_bt", "n_clicks"),
    prevent_initial_call=True,
)

def scatter_info():
    return (scatter_content(), scatter_layout())


@my_app.callback(
    Output("scatter", "is_open"),
    [Input("scatter_bt", "n_clicks")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open