# Adapted from https://dash.plotly.com/urls
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash import Input, Output

from multi_page_app.apps.app1 import recycle_app
from multi_page_app.apps.app2 import app2

from multi_page_app.app import app

# Add the navbar code here
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="/app1"), id="app-1-link"),
        dbc.NavItem(dbc.NavLink("Page 2", href="/app2"), id="app-2-link")
    ],
    brand="Multi page app example",
    brand_href="/",
    color="primary",
    dark=True,
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])

index_layout = html.Div([
    html.P('This is a multi-page Dash app')
])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/app1':
        return recycle_app.layout
    elif pathname == '/app2':
        return app2.layout
    elif pathname == '/':
        return index_layout
    else:
        return '404 Page Not Found'


if __name__ == '__main__':
    app.run_server(debug=True)
