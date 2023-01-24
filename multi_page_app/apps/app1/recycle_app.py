import dash_bootstrap_components as dbc
from dash import dcc, Output, Input
from dash import html

from multi_page_app.apps.app1.recyclingchart import RecyclingChart
from multi_page_app.apps.app1.recyclingdata import RecyclingData

from multi_page_app.app import app

# Prepare the data set
data = RecyclingData()
area = 'London'
data.process_data_for_area(area)

# Create the figures
rc = RecyclingChart(data)
fig_rc = rc.create_chart(area)

# Create the app layout using Bootstrap fluid container
layout = dbc.Container(fluid=True, children=[
    dbc.Row(
        dbc.Col(children=[html.Br(),
                          html.H1('Waste and recycling'),
                          html.P(
                              'Turn London waste into an opportunity – by reducing waste, reusing and recycling '
                              'more of it.',
                              className='lead')
                          ]),
    ),
    dbc.Row([
        dbc.Col(width=3, children=[
            html.H4("Select Area"),
            dcc.Dropdown(id="area-select",
                         options=[{"label": x, "value": x} for x in data.area_list],
                         value="London"),
            html.Br(),
            html.Div(id="stats-card"),
        ]),
        dbc.Col(width=9, children=[
            html.H2('Recycling'),
            dcc.Graph(id='recycle-chart', figure=fig_rc),
        ]),
    ]),
])


# Create the callbacks
@app.callback(Output("stats-card", "children"), [Input("area-select", "value")])
def render_output_panel(area_select):
    data.process_data_for_area(area_select)
    card = html.Div([
        dbc.Card(className="bg-dark text-light", children=[
            dbc.CardBody([
                html.H4(area_select, id="card-name", className="card-title"),
                html.Br(),
                html.H6("Compared to England:", className="card-title"),
                html.H4("{:,.0f}%".format(data.compare_to_eng), className="card-text text-light"),
                html.Br(),
                html.H6("Compared to previous year:".format(area=area), className="card-title"),
                html.H4("{:,.0f}%".format(data.change_area), className="card-text text-light"),
                html.Br(),
                html.H6("Best period:", className="card-title"),
                html.H4(data.best_period, className="card-text text-light"),
                html.H6("with recycling rate {:,.0f}%".format(data.best_rate), className="card-title text-light"),
                html.Br()
            ])
        ])
    ])
    return card


@app.callback(Output("recycle-chart", "figure"), [Input("area-select", "value")])
def update_recycling_chart(area_select):
    fig_rc = rc.create_chart(area_select)
    return fig_rc
