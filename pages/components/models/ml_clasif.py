# dash imports
import dash
from dash import html
from dash import Input
from dash import Output
from dash import dcc
import dash_bootstrap_components as dbc
from dash import State
import pandas as pd
from datetime import date
from dash.exceptions import PreventUpdate

# file imports
from maindash import my_app, df, models

risk_labels = {
    0: 'Riesgo Moderado',
    1: 'Riesgo Alto',
    2: 'Riesgo Bajo'
}

def get_recommendations(risk, age_group):
    recommendations = {
        'Riesgo Alto': {
            'ADULTOS': [
                "Verificación del bienestar por parte de las autoridades y servicios sociales.",
                "Acceso a consejería legal y psicológica para evaluar las opciones disponibles.",
                "Ofrecer programas de mediación y resolución de conflictos si se considera seguro.",
                "Seguimiento continuo del caso para evaluar cualquier escalada en el riesgo."
            ],
            'ADOLESCENTES': [
                "Intervención policial y evaluación de seguridad, incluyendo la posibilidad de reubicación temporal.",
                "Apoyo psicológico especializado para adolescentes, considerando el impacto en su desarrollo y educación.",
                "Involucrar servicios de protección infantil si se considera necesario.",
                "Crear un plan de seguridad personalizado que incluya aspectos de su vida social y escolar."
            ],
            'MENORES': [
                "* Garantizar la seguridad inmediata del niño con la intervención de la policía y servicios de protección infantil.",
                "* Evaluaciones psicológicas regulares para identificar traumas y ofrecer intervenciones tempranas.",
                "* Reubicación en un entorno seguro si es necesario, considerando hogares de acogida o el cuidado de familiares directos.",
                "* Programas de apoyo emocional y social adaptados a su edad."
            ]
        },
        'Riesgo Moderado': {
            'ADULTOS': [
                "Verificación del bienestar por parte de las autoridades y servicios sociales.",
                "Acceso a consejería legal y psicológica para evaluar las opciones disponibles.",
                "Ofrecer programas de mediación y resolución de conflictos si se considera seguro.",
                "Seguimiento continuo del caso para evaluar cualquier escalada en el riesgo."
            ],
            'ADOLESCENTES': [
                "Supervisión y seguimiento regular por parte de trabajadores sociales o consejeros escolares.",
                "Talleres sobre relaciones saludables y habilidades de afrontamiento.",
                "Asesoramiento psicológico adaptado a necesidades adolescentes.",
                "Evaluación constante para asegurar que el ambiente en el hogar es seguro."

            ],
            'MENORES': [
                 "Seguimiento periódico del bienestar del niño por parte de trabajadores sociales.",
                 "Programas educativos y de apoyo adaptados a su nivel de desarrollo.",
                 "Terapia de juego o terapias artísticas para ayudar en la expresión emocional y el manejo del estrés.",
                 "Asegurar que la escuela esté informada y pueda proporcionar un entorno de apoyo."
            ]
        },
        'Riesgo Bajo': {
            'ADULTOS': [
                "Ofrecer recursos informativos sobre los signos de abuso y cómo buscar ayuda.",
                "Acceso a líneas de ayuda y asesoramiento psicológico no urgente.",
                "Programas educativos sobre relaciones saludables y comunicación efectiva.",
                "Monitoreo discreto y seguimiento para prevenir escaladas."
            ],
            'ADOLESCENTES': [
                "Talleres educativos en escuelas sobre el reconocimiento de relaciones abusivas.",
                "Líneas de ayuda y soporte específico para adolescentes.",
                "Actividades y grupos de apoyo para fomentar la autoestima y habilidades de vida."

            ],
            'MENORES': [
                 "Programas en escuelas sobre seguridad personal y reconocimiento de situaciones abusivas.",
                 "Apoyo emocional a través de actividades grupales o terapia de juego.",
                 "Asegurar un ambiente estable en el hogar y en la escuela, con adultos de confianza disponibles para apoyo."
            ]
        }
    }
    
    risk_group = recommendations.get(risk, {})
    return " Recomendaciones: " + " ".join(risk_group.get(age_group, []))

def clasif_content():
    return html.Div([
        html.Div([html.H3("🧠 Seleccionar Modelo")]),
        dcc.Dropdown(
            id="model_selector",
            options=[{"label": key, "value": key} for key in models.keys()],
            value="Random Forest",
        ),
        html.Br(),
         dcc.Dropdown(
            id="departamento_input",
            options=[{'label': dept, 'value': dept} for dept in df['departamento'].unique()],
            placeholder="Selecciona un departamento",
        ),
        html.Br(),
        dcc.Dropdown(
            id="municipio_input",
            placeholder="Selecciona un municipio",
        ),
        html.Br(),
        dcc.Dropdown(
            id="armas_medios_input",
            options=[{'label': arma, 'value': arma} for arma in df['armas_medios'].unique()],
            placeholder="Selecciona arma/medio",
        ),
        html.Br(),
        dcc.DatePickerSingle(
            id='fecha_hecho_input',
            min_date_allowed=date(2024, 3, 1),
            initial_visible_month=date(2024, 3, 1),
        ),
        html.Br(),
        dcc.Dropdown(
            id="genero_input",
            options=[{'label': gen, 'value': gen} for gen in df['genero'].unique()],
            placeholder="Selecciona género",
        ),
        html.Br(),        
        dcc.Dropdown(
            id="grupo_etario_input",
            options=[{'label': grupo, 'value': grupo} for grupo in df['grupo_etario'].unique()],
            placeholder="Selecciona grupo etario",
        ),
        html.Br(),
        dbc.Input(
            type="number",
            id="cantidad_input",
            placeholder="Ingresa la cantidad",
            min=1,
            step=1,
        ),
        html.Br(),
        dbc.Button(
            "Clasificar Nivel de Riesgo",
            color="success",
            className="me-1",
            id="predict_button",
            n_clicks=0,
        ),
        html.Br(),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Resultado de la Predicción")),
                dbc.ModalBody(html.Div(id="prediction_output")),
                dbc.ModalFooter(dbc.Button("Cerrar", id="close_modal", className="ml-auto")),
            ],
            id="prediction_modal",
            is_open=False,
        ),
    ])

def clasif_layout():
    return dbc.Container([
        html.Div([
            html.Div([
                html.Img(
                    src="https://images.unsplash.com/photo-1649393832219-0ad856a1e119?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                    style={"width": "100%", "height": "auto", "position": "relative"},
                ),
            ], style={"height": "200px", "overflow": "hidden", "position": "relative"}),
            html.H1("Clasificación de Riesgos", style={
                "position": "absolute",
                "top": "80%",
                "left": "50%",
                "transform": "translate(-50%, -50%)",
                "color": "white",
                "text-align": "center",
                "width": "100%",
            }),
        ], style={"position": "relative", "text-align": "center", "color": "white", "height": "200px"}),
        html.Br(),
        dbc.Row([
            dbc.Col(html.Div([clasif_content()]), width=4),
            dbc.Col(html.Div(id="prediction_results"), width=8),
        ], className='g-0'),
        html.Br(),
    ], fluid=True)

@my_app.callback(
    Output('municipio_input', 'options'),
    Input('departamento_input', 'value')
)

def set_municipios_options(selected_departamento):
    filtered_df = df[df['departamento'] == selected_departamento]
    return [{'label': i, 'value': i} for i in filtered_df['municipio'].unique()]

@my_app.callback(
    Output("prediction_results", "children"),
    [Input("predict_button", "n_clicks")],
    [State("model_selector", "value"),
     State("departamento_input", "value"), State("municipio_input", "value"),
     State("armas_medios_input", "value"), State("fecha_hecho_input", "date"),
     State("genero_input", "value"), State("grupo_etario_input", "value"),
     State("cantidad_input", "value")]
)


def update_prediction_output(n_clicks, selected_model, departamento, municipio, armas_medios, fecha_hecho, genero, grupo_etario, cantidad):
    if not n_clicks:
        raise PreventUpdate

    if not all([departamento, municipio, armas_medios, fecha_hecho, genero, grupo_etario, cantidad]):
        return html.Div("Por favor complete todos los campos para hacer una predicción.")

    input_data = pd.DataFrame([[
        departamento, municipio, armas_medios, fecha_hecho, genero, grupo_etario, cantidad
    ]], columns=['departamento', 'municipio', 'armas_medios', 'fecha_hecho', 'genero', 'grupo_etario', 'cantidad'])

    model = models[selected_model]
    prediction = model.predict(input_data)[0]
    risk_description = risk_labels[prediction]

    recommendations = get_recommendations(risk_description, grupo_etario)
    
    results_layout = html.Div([
        html.H2(f"Predicción: {risk_description}", style={"color": "#888"}),
        html.H3("Recomendaciones:", style={"color": "#888"}),
        html.Ul([html.Li(rec) for rec in recommendations.split(" Recomendaciones: ")[1].split(". ") if rec])
    ], style={"margin-left": "20px"})
    
    return results_layout

def clasif_info():
    return (clasif_content(), clasif_layout())