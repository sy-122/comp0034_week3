from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

from recycle_app.recyclingchart import RecyclingChart
from recycle_app.recyclingdata import RecyclingData

# Prepare the data set
data = RecyclingData()
area = "London"
data.process_data_for_area(area)

# Create the figures
rc = RecyclingChart(data)
fig_rc = rc.create_chart(area)

# Create a Dash app (using bootstrap).
app = Dash(
    external_stylesheets=[dbc.themes.LUX],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
)

# Create the app layout using Bootstrap fluid container
app.layout = dbc.Container(
    fluid=True,
    children=[
        html.Br(),
        html.H1("Waste and recycling"),
        html.P(
            "Turn London waste into an opportunity – by reducing waste, reusing and recycling more of it.",
            className="lead",
        ),
        html.H2("Recycling"),
        dcc.Graph(id="recycle-chart", figure=fig_rc),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)
