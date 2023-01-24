from dash import html, dcc, Dash, dash_table
import dash_bootstrap_components as dbc
from paralympics_app import create_charts as cc

fig_line_sports = cc.line_chart_sports()
fig_sb_gender_winter = cc.stacked_bar_gender("Winter")
fig_sb_gender_summer = cc.stacked_bar_gender("Summer")
fig_scatter_mapbox = cc.scatter_mapbox_para_locations("OSM")
df_medals_data = cc.top_ten_gold_data()
df_medals = cc.get_medals_table_data("London", 2012)
fig_cp_map_medals = cc.choropleth_mapbox_medals(df_medals)

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
)

app.layout = dbc.Container(
    [
        html.H1("Paralympic History"),
        html.H2(
            "Has the number of athletes, nations, events and sports changed over time?"
        ),
        dcc.Graph(id="line-sports", figure=fig_line_sports),
        html.H2(
            "Has the ratio of male and female athletes changed over time?"
        ),
        dcc.Graph(id="stacked-bar-gender-win", figure=fig_sb_gender_winter),
        dcc.Graph(id="stacked-bar-gender-sum", figure=fig_sb_gender_summer),
        html.H2("Where in the world have the Paralympics have been held?"),
        dcc.Graph(id="scatter-mapbox-osm", figure=fig_scatter_mapbox),
        html.H2("Which countries have won the most gold medals since 1960?"),
        dash_table.DataTable(
            id="table-top-ten-gold-dash",
            columns=[{"name": i, "id": i} for i in df_medals_data.columns],
            data=df_medals_data.to_dict("records"),
            style_cell=dict(textAlign="left"),
            style_header=dict(backgroundColor="lightskyblue"),
            style_data=dict(backgroundColor="white"),
        ),
        html.H2("What is the medal performance of each country?"),
        html.P("Medal performance in London 2012"),
        dcc.Graph(id="cp-map-medals", figure=fig_cp_map_medals),
    ],
    fluid=True,
)

if __name__ == "__main__":
    app.run_server(debug=True, port=8555)
