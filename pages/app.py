# dash imports
import dash
from dash import html
from dash import Input
from dash import Output
from dash import dcc
import dash_bootstrap_components as dbc
import os
import sys
import warnings
from pandas.errors import PerformanceWarning
from sklearn.exceptions import ConvergenceWarning
warnings.filterwarnings('ignore', category=FutureWarning)
warnings.filterwarnings('ignore', category=PerformanceWarning)
warnings.filterwarnings('ignore', category=ConvergenceWarning)
warnings.filterwarnings('ignore', message="Trying to unpickle estimator*")
import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning, message='divide by zero encountered in log10')
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=FutureWarning)


# file imports
from maindash import my_app
from components.overview import overview
from components.analysis import analysis
from components.casos import casos
from components.about import about
from components.overview import overview
from components.models import ml_clasif
from components.models import ml_reg

#######################################
# Initial Settings
#######################################
server = my_app.server

CONTENT_STYLE = {
    "transition": "margin-left .1s",
    "padding": "1rem 1rem",
}

#######################################
# Layout
########################################
sidebar = html.Div(
    [
        html.Div(
            [
                html.H2("VDC", style={"color": "white"}),
            ],
            className="sidebar-header",
        ),
        html.Br(),
        html.Div(style={"border-top": "2px solid white"}),
        html.Br(),
        # nav component
        dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.I(className="fas fa-solid fa-star me-2"),
                        html.Span("Descripción General"),
                    ],
                    href="/",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-home me-2"),
                        html.Span("Casos Reportados"),
                    ],
                    href="/casos",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-solid fa-chart-simple me-2"),
                        html.Span("Análisis Exploratorio"),
                    ],
                    href="/analysis",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-solid fa-people-group me-2"),
                        html.Span("Clasificación de Riesgo"),
                    ],
                    href="/clasif",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-solid fa-arrow-trend-up me-2"),
                        html.Span("Métricas Modelos"),
                    ],
                    href="/prediction",
                    active="exact",
                ),
                dbc.NavLink(
                    [
                        html.I(className="fas fa-solid fa-code me-2"),
                        html.Span("Info"),
                    ],
                    href="/about",
                    active="exact",
                )
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
)


my_app.layout = html.Div(
    [
        dcc.Location(id="url"),
        sidebar,
        html.Div(
            [
                dash.page_container,
            ],
            className="content",
            style=CONTENT_STYLE,
            id="page-content",
        ),
    ]
)


@my_app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return overview.overview_layout()
    elif pathname == "/casos":
        return casos.casos_layout()
    elif pathname == "/analysis":
        return analysis.analysis_layout()
    elif pathname == "/clasif":
        return ml_clasif.clasif_layout()
    elif pathname == "/prediction":
        return ml_reg.reg_layout()
    elif pathname == "/about":
        return about.about_layout()
    return dbc.Container(
        children=[
            html.H1(
                "404 Error: Page Not found",
                style={"textAlign": "center", "color": "#082446"},
            ),
            html.Br(),
            html.P(
                f"Oh no! The pathname '{pathname}' was not recognised...",
                style={"textAlign": "center"},
            ),
            # image
            html.Div(
                style={"display": "flex", "justifyContent": "center"},
                children=[
                    html.Img(
                        src="https://elephant.art/wp-content/uploads/2020/02/gu_announcement_01-1.jpg",
                        alt="hokie",
                        style={"width": "400px"},
                    ),
                ],
            ),
        ]
    )


if __name__ == "__main__":
    my_app.run_server(debug=True)