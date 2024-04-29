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
table_department = df.groupby('departamento')['cantidad'].sum().reset_index()
table_department = table_department.rename(columns={'cantidad': 'total_cantidad'})
table_department_sorted = table_department.sort_values(by='total_cantidad', ascending=False)
locs = table_department['departamento']
for loc in counties['features']:
    loc['id'] = loc['properties']['NOMBRE_DPT']

fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=['Normal distribution', 'Logarithm 10'],
    specs=[[{"type": "mapbox"}, {"type": "mapbox"}]]
)

fig.add_trace(
    go.Choroplethmapbox(
        geojson=counties,
        locations=table_department['departamento'],
        z=table_department['total_cantidad'],
        colorbar_title='Casos',
        colorscale='YlOrRd',
        colorbar=dict(thickness=20, x=0.46),
        marker=dict(opacity=0.75)
    ),
    row=1, col=1
)

fig.add_trace(
    go.Choroplethmapbox(
        geojson=counties,
        locations=table_department['departamento'],
        z=log10(table_department['total_cantidad']),
        colorbar_title='Case count (Log10)',
        colorscale='YlOrRd',
        colorbar=dict(thickness=20, x=1.02),
        marker=dict(opacity=0.75)
    ),
    row=1, col=2
)

fig.update_layout(
    margin=dict(l=20, r=0, t=80, b=40),
    title='Casos de Violencia doméstica distribuidos en Colombia',
    mapbox1=dict(zoom=3.4, style='carto-positron', center={"lat": 4.570868, "lon": -74.2973328}),
    mapbox2=dict(zoom=3.4, style='carto-positron', center={"lat": 4.570868, "lon": -74.2973328})
)


def mapdep1_layout():
    layout = html.Div(
        [
            dcc.Loading(children=[dcc.Graph(figure=fig)]),
        ]
    )
    return layout


def mapdep1_content():
    return html.Div(
        [
            html.Div([html.H3("👁‍🗨 Observaciones")]),
            html.Div(
                [
                    html.P(
                        "Los casos reportados están concentrados en la parte central del país"
                    )
                ]
            ),
        ]
    )


@my_app.callback(
    Output("mapdep1", "data"),
    Input("mapdep1_bt", "n_clicks"),
    prevent_initial_call=True,
)

def mapdep1_info():
    return (mapdep1_content(), mapdep1_layout())


@my_app.callback(
    Output("mapdep1", "is_open"),
    [Input("mapdep1_bt", "n_clicks")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open