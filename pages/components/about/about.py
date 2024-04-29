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
def about_layout():
    layout = html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.Img(
                                src="https://images.unsplash.com/photo-1614854262340-ab1ca7d079c7?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
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
                        "Info",
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
            html.Div(
                style={"display": "flex"},
                children=[
                    dcc.Markdown(
                        children=read_file_as_str("./Utils/Markdown/about/about.md"),
                        mathjax=True,
                    ),
                ],
            ),
            card(),
        ]
    )

    return layout


def card():
    layout = html.Div(
        [
            html.Br(),
            dbc.Card(
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.CardImg(
                                src="https://media.licdn.com/dms/image/D4E03AQG5z1JtyicK1g/profile-displayphoto-shrink_200_200/0/1698248620739?e=2147483647&v=beta&t=V5ZeFEKgEKNFv9p1CJS6wfC7lq2VGWEG8eQ2UcinyQ4",
                                className="img-fluid rounded-start",
                            ),
                            className="col-md-4",
                        ),
                        dbc.Col(
                            dbc.CardBody(
                                [
                                    html.H4("Lisa M. Puche", className="card-title"),
                                    html.P([
                                        "Economista, ",
                                        html.Br(),
                                        "M.Sc. Analítica de Datos, ",
                                        html.Br(),
                                        "Universidad del Norte"
                                    ], className="card-text"),
                                    html.Small("lisap@uninorte.edu.co", className="card-text text-muted"),
                                    html.Br(),
                                    html.A(
                                        html.Img(
                                            src="https://cdn-icons-png.flaticon.com/512/174/174857.png",
                                            alt="LinkedIn",
                                            style={"width": "30px", "height": "30px", "marginRight": "10px"},
                                        ),
                                        href="https://co.linkedin.com/in/lisapuche",
                                        target="_blank",
                                        className="text-dark",
                                    ),
                                    html.A(
                                        html.Img(
                                            src="https://cdn-icons-png.flaticon.com/512/25/25231.png",
                                            alt="GitHub",
                                            style={"width": "30px", "height": "30px"},
                                        ),
                                        href="https://github.com/mnguyen0226",
                                        target="_blank",
                                        className="text-dark",
                                    ),
                                ]
                            ),
                            className="col-md-8",
                        ),
                    ],
                    className="g-0 d-flex align-items-center",
                ),
                className="mb-3",
                style={"maxWidth": "540px"},
            ),
            dbc.Card(
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.CardImg(
                                src="https://media.licdn.com/dms/image/D4E03AQGyRuU88yEL7w/profile-displayphoto-shrink_400_400/0/1697743842939?e=1719446400&v=beta&t=fzI3eMe82CVvItJx-UGLB4z5WHDVk6d7JjLpy_MR9f0",
                                className="img-fluid rounded-start",
                            ),
                            className="col-md-4",
                        ),
                        dbc.Col(
                            dbc.CardBody(
                                [
                                    html.H4("Andrés F. Vargas", className="card-title"),
                                    html.P([
                                        "Economista, ",
                                        html.Br(),
                                        "M.Sc. Analítica de Datos, ",
                                        html.Br(),
                                        "Universidad del Norte"
                                    ], className="card-text"),
                                    html.Small("afhumanez@uninorte.edu.co", className="card-text text-muted"),
                                    html.Br(),
                                    html.A(
                                        html.Img(
                                            src="https://cdn-icons-png.flaticon.com/512/174/174857.png",
                                            alt="LinkedIn",
                                            style={"width": "30px", "height": "30px", "marginRight": "10px"},
                                        ),
                                        href="https://www.linkedin.com/in/andvar7",
                                        target="_blank",
                                        className="text-dark",
                                    ),
                                    html.A(
                                        html.Img(
                                            src="https://cdn-icons-png.flaticon.com/512/25/25231.png",
                                            alt="GitHub",
                                            style={"width": "30px", "height": "30px"},
                                        ),
                                        href="https://github.com/andvar7",
                                        target="_blank",
                                        className="text-dark",
                                    ),
                                ]
                            ),
                            className="col-md-8",
                        ),
                    ],
                    className="g-0 d-flex align-items-center",
                ),
                className="mb-3",
                style={"maxWidth": "540px"},)
        ]
    )
    return layout
