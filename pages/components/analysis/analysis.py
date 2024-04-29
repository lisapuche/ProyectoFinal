# dash imports
import dash
from dash import html
from dash import Input
from dash import Output
from dash import dcc
import dash_bootstrap_components as dbc

# file imports
from maindash import my_app
from components.analysis.distribucion import distribucion_info
from components.analysis.historico import historico_info
from components.analysis.scatter import scatter_info
from components.analysis.arma import arma_info
from components.analysis.piechart import pie_info
from components.analysis.genero_arma import barsex_info
from components.analysis.sex_age import sexage_info
from components.analysis.escop import dep_info
from components.analysis.mapa_escop import mapdep_info
from components.analysis.series import series_info
from components.analysis.series1 import series1_info
from components.analysis.corr import corr_info
from components.analysis.map1 import mapdep1_info

#######################################
# Layout
#######################################
def analysis_layout():
    layout = html.Div(
        [
            # image
            html.Div(
                [
                    html.Div(
                        [
                            html.Img(
                                src="https://images.unsplash.com/photo-1614851099511-773084f6911d?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                                style={
                                    "width": "100%",
                                    "height": "auto",
                                    "position": "relative",
                                },
                            ),
                        ],
                        style={
                            "height": "200px",
                            "overflow": "hidden",
                            "position": "relative",
                        },
                    ),
                    html.H1(
                        "Análisis Exploratorio",
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
                ],
                style={
                    "position": "relative",
                    "text-align": "center",
                    "color": "white",
                },
            ),
            html.Br(),
            # tab
            html.Div(
                style={"display": "flex"},
                children=[
                    html.Div(
                        [
                            dbc.Tabs(
                                id="analysis_selected_tab",
                                children=[
                                    dbc.Tab(
                                        label="Histogramas",
                                        tab_id="distribucion",
                                    ),
                                    dbc.Tab(
                                        label="Map Dpto",
                                        tab_id="map_distribucion",
                                    ),
                                    dbc.Tab(
                                        label="Line Plot Casos",
                                        tab_id="histo_line",
                                    ),
                                    dbc.Tab(
                                        label="Scatter Región",
                                        tab_id="scatter",
                                    ),
                                    dbc.Tab(
                                        label="Bar plot Armas",
                                        tab_id="bar_plot1",
                                    ),
                                    dbc.Tab(
                                        label="Pie Chart Género",
                                        tab_id="pie_chart1",
                                    ),
                                    dbc.Tab(
                                        label="Bar Plot Género-Arma",
                                        tab_id="bar_sex1",
                                    ),
                                    dbc.Tab(
                                        label="Bar plot Género-Edad",
                                        tab_id="bar_sexage1",
                                    ),
                                    dbc.Tab(
                                        label="Bar plot Dpto",
                                        tab_id="bar_dpto1",
                                    ),
                                    dbc.Tab(
                                        label="Mapa ArmaFuego",
                                        tab_id="map_escop",
                                    ),
                                    dbc.Tab(
                                        label="Bar plot Mes/Dia",
                                        tab_id="bar_mes",
                                    ),
                                    dbc.Tab(
                                        label="Series",
                                        tab_id="serie_mes",
                                    ),
                                    dbc.Tab(
                                        label="Heatmap",
                                        tab_id="corr",
                                    ),  
                                ],
                                active_tab="analysis_line",
                            ),
                        ]
                    ),
                ],
            ),
            html.Br(),
            # content: analysis & plot
            html.Div(
                style={"display": "flex"},
                children=[
                    html.Div(
                        style={
                            "width": "30%",
                            "padding": "10px",
                        },
                        children=[
                            html.Div(id="analysis_tab_content_layout"),
                        ],
                    ),
                    html.Div(
                        style={
                            "width": "70%",
                            "padding": "10px",
                        },
                        children=[
                            html.Div(id="analysis_tab_plot_layout"),
                        ],
                    ),
                ],
            ),
        ]
    )

    return layout


#######################################
# Callbacks
#######################################
@my_app.callback(
    [
        Output(
            component_id="analysis_tab_content_layout", component_property="children"
        ),
        Output(component_id="analysis_tab_plot_layout", component_property="children"),
    ],
    [Input(component_id="analysis_selected_tab", component_property="active_tab")],
)
def render_tab(tab_choice):
    """Renders the selected subtab's layout

    Args:
        tab_choice (str): selected subtab

    Returns:
        selected subtab's layout
    """
    if tab_choice == "distribucion":
        return distribucion_info()
    if tab_choice == "map_distribucion":
        return mapdep1_info()
    if tab_choice == "histo_line":
        return historico_info()
    if tab_choice == "scatter":
        return scatter_info()
    if tab_choice == "bar_plot1":
        return arma_info()
    if tab_choice == "pie_chart1":
        return pie_info()
    if tab_choice == "bar_sex1":
        return barsex_info()
    if tab_choice == "bar_sexage1":
        return sexage_info()
    if tab_choice == "bar_dpto1":
        return dep_info() 
    if tab_choice == "map_escop":
        return mapdep_info()
    if tab_choice == "bar_mes":
        return series_info()
    if tab_choice == "serie_mes":
        return series1_info()      
    if tab_choice == "corr":
        return corr_info()   
    else:
        # Return a default layout or message when no tab matches
        return html.Div("Seleccione una pestaña."), None