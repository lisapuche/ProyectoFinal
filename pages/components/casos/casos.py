import dash
import pandas as pd
from dash import html, dcc, Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from math import log10

# file imports
from maindash import my_app, df,counties

df['fecha_hecho'] = pd.to_datetime(df['fecha_hecho'])
#######################################
# Layout
####################################### 

def casos_layout():
    layout = html.Div([
        html.Div([
            html.Img(
                src="https://images.unsplash.com/photo-1614851099511-773084f6911d?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                style={"width": "100%", "height": "200px", "position": "relative"},
            ),
            html.H1(
                "Casos Reportados en Colombia",
                style={
                    "position": "absolute",
                    "top": "80%",
                    "left": "50%",
                    "transform": "translate(-50%, -50%)",
                    "color": "white",
                    "text-align": "center",
                    "width": "100%",
                },
            ),
        ], style={"position": "relative", "text_align": "center", "color": "white", "height": "200px"}),

        html.Br(),

        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H3("Filtros"),
                    dcc.DatePickerRange(
                        id='filter-date',
                        start_date=df['fecha_hecho'].min(),
                        end_date=df['fecha_hecho'].max(),
                        display_format='DD/MM/YYYY',
                        start_date_placeholder_text="Inicio",
                        end_date_placeholder_text="Fin"
                    ),
                    dcc.Dropdown(
                        id='filter-department',
                        options=[{'label': dept, 'value': dept} for dept in df['departamento'].unique()],
                        value=None,
                        multi=True,
                        placeholder="Seleccione Departamento(s)"
                    ),
                    dcc.Dropdown(
                        id='filter-gender',
                        options=[{'label': gen, 'value': gen} for gen in df['genero'].unique()],
                        value=None,
                        multi=True,
                        placeholder="Seleccione Género(s)"
                    ),
                    dcc.Dropdown(
                        id='filter-weapon',
                        options=[{'label': weapon, 'value': weapon} for weapon in df['armas_medios'].unique()],
                        value=None,
                        multi=True,
                        placeholder="Seleccione Arma(s) o Medio(s)"
                    ),
                ]),
            ], width=3),
            dbc.Col([
                dcc.Graph(id='map-display', style={"height": "500px"}),
            ], width=9),
        ]),
    ])
    return layout

@my_app.callback(
    Output('map-display', 'figure'),
    [Input('filter-date', 'start_date'),
     Input('filter-date', 'end_date'),
     Input('filter-department', 'value'),
     Input('filter-gender', 'value'),
     Input('filter-weapon', 'value')]
)
def update_map(start_date, end_date, selected_departments, selected_genders, selected_weapons):
    filtered_df = df.copy()
    if start_date and end_date:
        filtered_df = filtered_df[(filtered_df['fecha_hecho'] >= start_date) & (filtered_df['fecha_hecho'] <= end_date)]
    if selected_departments:
        filtered_df = filtered_df[filtered_df['departamento'].isin(selected_departments)]
    if selected_genders:
        filtered_df = filtered_df[filtered_df['genero'].isin(selected_genders)]
    if selected_weapons:
        filtered_df = filtered_df[filtered_df['armas_medios'].isin(selected_weapons)]

    aggregated_data = filtered_df.groupby('departamento')['cantidad'].sum().reset_index()

    fig = go.Figure(
        go.Choroplethmapbox(
            geojson=counties, 
            locations=aggregated_data['departamento'],
            z=aggregated_data['cantidad'],
            colorbar_title='Casos',
            colorscale='YlOrRd',
            marker=dict(opacity=0.75)
        )
    )
    fig.update_layout(
        mapbox_style='carto-positron',
        mapbox_zoom=3.9,
        mapbox_center={"lat": 4.570868, "lon": -74.2973328}
    )
    return fig