from pathlib import Path
from dash import html, dcc, Dash
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from lollapalooza_app import prepare_data


# -------
# Charts
# -------

# Purchases chart
file_path = Path(__file__).parent.joinpath("data", "purchase_data.csv")
df_purchase = pd.read_csv(file_path)
df_purchase_prepared = prepare_data.prepare_purchase_data(df_purchase)
fig_bar = px.bar(
    df_purchase_prepared,
    x="spend",
    y="date",
    color="place",
    title="Purchases by place",
)

# Heatmap chart
heatmap_df = prepare_data.prepare_purchase_data_heatmap(df_purchase)
fig_heatmap = px.imshow(heatmap_df, title="Purchases by hour heatmap")

# Mapbox chart (px)
file_path_stages = Path(__file__).parent.joinpath("data", "stages.csv")
df_stages = pd.read_csv(file_path_stages)

fig_map = px.scatter_mapbox(
    df_stages,
    lat="latitude",
    lon="longitude",
    color="stage",
    center=dict(lat=-23.701057, lon=-46.6970635),
    hover_name="stage",
    zoom=15.5,
    mapbox_style="open-street-map",
    title="Lollapalooza Brazil 2018 map",
)


# Mapbox chart (go)

# mapbox_token = "" # Add your mapbox token here between the speech marks and remove the next line
mapbox_token = open(Path(__file__).parent.joinpath("mapbox_token.txt")).read()

trace = go.Scattermapbox(
    lat=df_stages["latitude"],
    lon=df_stages["longitude"],
    text=df_stages["stage"],
    marker={"size": 20},
    mode="markers+text",
    textposition="top left",
)

data = [trace]

layout = go.Layout(
    mapbox=dict(
        accesstoken=mapbox_token,
        center=dict(lat=-23.701057, lon=-46.6970635),
        zoom=14.5,
    )
)

fig_map_go = go.Figure(data=data, layout=layout)


# Table of concerts (go)
file_path_concert = Path(__file__).parent.joinpath(
    "data", "concerts_I_attended.csv"
)
df_table = pd.read_csv(file_path_concert)
df_table = prepare_data.prepare_concert_data(df_table)
trace_table = go.Table(
    header=dict(
        values=["Concert", "Date", "Correct?"],
        fill=dict(color=("rgb(82,187,47)")),
    ),
    cells=dict(
        values=[df_table.concert, df_table.date, df_table.correct],
        font=dict(color=([df_table.color])),
    ),
)

data = [trace_table]
fig_table = go.Figure(data=data)

# ----------
# Dash app
# ----------

app = Dash(__name__)

app.layout = html.Div(
    children=[
        html.H1("Lollapalooza experience"),
        html.H2("How did she spend her money?"),
        dcc.Graph(id="spend-bar-graph", figure=fig_bar),
        dcc.Graph(id="spend-heatmap", figure=fig_heatmap),
        html.H2("Where did she go?"),
        dcc.Graph(id="fig-scatterbox-map", figure=fig_map),
        html.P("Plotly go version"),
        dcc.Graph(id="fig-scatterbox-map-go", figure=fig_map_go),
        html.H2("Which concerts did she watch?"),
        dcc.Graph(id="fig-concerts", figure=fig_table),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
