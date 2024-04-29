import plotly.express as px
from dash import html, Input, Output, dcc, State
import pandas as pd
from numpy import log10
import dash_bootstrap_components as dbc
from scipy.stats import probplot
import plotly.graph_objs as go
from plotly.subplots import make_subplots

# file imports
from maindash import my_app
from maindash import df,counties
from Utils.file_operation import read_file_as_str

#Grafico
dfsco = df.query('armas_medios == "ARMA DE FUEGO"')
dfdsco = pd.pivot_table(dfsco, index = 'departamento', values = 'cantidad', columns = None, aggfunc='count').reset_index()
dfdsco['departamento'] = dfdsco['departamento'].replace({'ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA': 'SAN ANDRES'})

locs = dfdsco['departamento']
for loc in counties['features']:
    loc['id'] = loc['properties']['NOMBRE_DPT']

fig = go.Figure(go.Choroplethmapbox(
    geojson=counties,
    locations=locs,
    z=log10(dfdsco['cantidad'].astype(float)),
    colorscale='YlOrRd',
    colorbar_title="Número"
))

fig.update_layout(
    mapbox_style="carto-positron",
    mapbox_zoom=3.9,
    mapbox_center={"lat": 4.570868, "lon": -74.2973328},
    title='Casos con Arma de Fuego distribuidos en el país Log10'
)


def mapdep_layout():
    layout = html.Div(
        [
            dcc.Loading(children=[dcc.Graph(figure=fig)]),
        ]
    )
    return layout


def mapdep_content():
    return html.Div(
        [
            html.Div([html.H3("👁‍🗨 Observaciones")]),
            html.Div(
                [
                    html.P(
                        "Distribución geográfica de los casos con Arma de Fuego en Colombia."
                    )
                ]
            ),
        ]
    )


@my_app.callback(
    Output("mapdep", "data"),
    Input("mapdep_bt", "n_clicks"),
    prevent_initial_call=True,
)

def mapdep_info():
    return (mapdep_content(), mapdep_layout())


@my_app.callback(
    Output("mapdep", "is_open"),
    [Input("mapdep_bt", "n_clicks")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open