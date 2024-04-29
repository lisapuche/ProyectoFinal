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
df_suma = df.groupby(pd.to_datetime(df['fecha_hecho']).dt.year)['cantidad'].sum().reset_index()
df_suma.columns = ['año', 'cantidad']

fig = px.line(df_suma, x='año', y='cantidad', title='Violencia Doméstica en Colombia', 
              hover_data={'año': True, 'cantidad': ':.0f'})

fig.update_xaxes(title='Año')
fig.update_yaxes(title='Cantidad de casos')

def historico_layout():
    layout = html.Div(
        [
            dcc.Loading(children=[dcc.Graph(figure=fig)]),
        ]
    )
    return layout


def historico_content():
    return html.Div(
        [
            html.Div([html.H3("👁‍🗨 Observaciones")]),
            html.Div(
                [
                    html.P(
                        "Hay una tendencia ascendente en la cantidad de casos reportados de violencia doméstica desde 2010 hasta aproximadamente 2018. Después de 2018, la tendencia se cambia y comienza a crecer para los años 2019 y 2020, hacia 2021 - 2023 se logra apreciar una disminución en los casos reportados."
                    )
                ]
            ),
        ]
    )


@my_app.callback(
    Output("historico", "data"),
    Input("historico_bt", "n_clicks"),
    prevent_initial_call=True,
)

def historico_info():
    return (historico_content(), historico_layout())


@my_app.callback(
    Output("historico", "is_open"),
    [Input("historico_bt", "n_clicks")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open