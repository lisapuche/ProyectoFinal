import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.figure_factory as ff
import plotly.graph_objects as go
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_curve
from sklearn.preprocessing import label_binarize
import pandas as pd
import numpy as np


from maindash import X_test, y_test, my_app, models

# Ensure y_test and y_pred are strings to avoid type issues
y_test_str = y_test.astype(str)

# App layout
def reg_layout():
    model_options = [{'label': name, 'value': name} for name in models.keys()]
    layout = html.Div([
        html.Div([
            html.Img(
                src="https://images.unsplash.com/photo-1649393832219-0ad856a1e119",
                style={"width": "100%", "height": "200px", "position": "relative"}
            ),
            html.H1("Model Evaluation", style={
                "position": "absolute",
                "top": "150px",
                "left": "50%",
                "transform": "translate(-50%, -50%)",
                "color": "white",
                "text-align": "center",
                "width": "100%"
            }),
        ], style={"position": "relative", "text_align": "center", "color": "white", "height": "200px"}),
        html.Br(),
        dcc.Dropdown(id='model-dropdown', options=model_options, value=list(models.keys())[0]),
        html.Div(id='model-output')
    ])
    return layout

# Update callback to include feature importance for XGBoost and ROC curves for all models
@my_app.callback(
    Output('model-output', 'children'),
    [Input('model-dropdown', 'value')]
)
def update_output(selected_model):
    # Prepare ROC curves for all models
    fig_roc = go.Figure()
    for model_name, model in models.items():
        y_proba = model.predict_proba(X_test)
        y_test_binarized = label_binarize(y_test, classes=np.unique(y_test))
        fpr, tpr, _ = roc_curve(y_test_binarized.ravel(), y_proba.ravel())
        fig_roc.add_trace(go.Scatter(x=fpr, y=tpr, mode='lines', name=f'ROC {model_name}'))
    fig_roc.update_layout(title='ROC Curve Comparison', xaxis_title='False Positive Rate', yaxis=dict(range=[0.98, 1.01]), yaxis_title='True Positive Rate')

    # Predictions and metrics for selected model
    model = models[selected_model]
    y_pred = model.predict(X_test)
    y_pred_str = y_pred.astype(str)
    accuracy = accuracy_score(y_test_str, y_pred_str)
    precision = precision_score(y_test_str, y_pred_str, average='weighted', zero_division=0)
    recall = recall_score(y_test_str, y_pred_str, average='weighted', zero_division=0)
    f1 = f1_score(y_test_str, y_pred_str, average='weighted', zero_division=0)
    labels = sorted(set(y_test_str).union(set(y_pred_str)))
    cm = confusion_matrix(y_test_str, y_pred_str, labels=labels)
    fig_cm = ff.create_annotated_heatmap(z=cm, x=labels, y=labels, colorscale='Blues')
    fig_cm.update_layout(title=f'Confusion Matrix for {selected_model}', xaxis_title='Predicted Label', yaxis_title='True Label')

    # Metrics table
    metrics_data = [
    {'Metric': 'Accuracy', 'Value': accuracy},
    {'Metric': 'Precision', 'Value': precision},
    {'Metric': 'Recall', 'Value': recall},
    {'Metric': 'F1 Score', 'Value': f1},
    ]

    metrics_table = dash_table.DataTable(
        columns=[
            {'name': 'Métrica', 'id': 'Metric'},
            {'name': 'Resultado', 'id': 'Value', 'type': 'numeric', 'format': {'specifier': '.4f'}}
        ],
        data=metrics_data,
        style_cell={'padding': '5px', 'textAlign': 'center', 'border': '1px solid black'},
        style_header={
            'backgroundColor': 'black',
            'fontWeight': 'bold',
            'textAlign': 'center',
            'color': 'white',
            'border': '1px solid black'
        },
        style_data={
            'border': '1px solid black'
        },
        style_data_conditional=[
            {'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(220, 220, 220)'}
        ]
    )

    # Feature importance for XGBoost
    components = [
        dcc.Graph(figure=fig_cm),
        metrics_table,
        dcc.Graph(figure=fig_roc)
    ]
    
    return components

my_app.layout = reg_layout
