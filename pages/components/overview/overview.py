# dash imports
import dash
from dash import html
from dash import Input
from dash import Output
from dash import dcc
import dash_bootstrap_components as dbc

# file imports
from maindash import my_app
from Utils.file_operation import read_file_as_str


#######################################
# Layout
#######################################
def overview_layout():
    layout = html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.Img(
                                src="https://images.unsplash.com/photo-1614850523425-eec693b15af5?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
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
                        "Descripción General",
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
            html.H3("🌟 Violencia Doméstica en Colombia"),
            html.Div(
                [
                    # Contenedor izquierdo para la imagen
                    html.Div(
                        [
                            dcc.Markdown(
                                children=read_file_as_str("Utils/Markdown/Overview/overview.md"),
                                mathjax=True,
                                style={
                                    "overflowY": "scroll",
                                    "maxHeight": "500px",
                                }
                            )
                        ],
                        style={"flex": "50%", "paddingLeft": "20px"}
                    ),
                    html.Div(
                        [
                            html.Img(
                                src="https://www.danielevasta.com/wp-content/uploads/2023/01/violencia-domestica.jpg",
                                style={
                                    "maxWidth": "80%",
                                    "maxHeight": "500px",
                                    "margin": "auto",
                                    "display": "block"
                                }
                            )
                        ],
                        style={"flex": "50%"}
                    )                   
                ],
                style={"display": "flex"}
            ),
            html.Br(),
        ]
    )
    return layout



