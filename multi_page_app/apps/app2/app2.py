# Copied from the Dash documetation sample code at https://github.com/plotly/dash-recipes/tree/master/multi-page-app
from dash import Input, Output, html, dcc
import dash_bootstrap_components as dbc
from multi_page_app.app import app

layout = dbc.Container(fluid=True, children=[
    html.Br(),
    html.H1('Fruit Selector'),
    dcc.Dropdown(
        id='app-2-dropdown',
        options=[
            {'label': '{}'.format(i), 'value': i} for i in [
                'Apple', 'Banana', 'Coconut', 'Date'
            ]
        ]
    ),
    html.Div(id='app-2-display-value')
])


@app.callback(Output('app-2-display-value', 'children'), Input('app-2-dropdown', 'value'))
def display_value(value):
    return 'You have selected "{}"'.format(value)
