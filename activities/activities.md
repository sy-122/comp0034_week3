# Introduction to interactivity in Dash

Contents:

- [Introduction to this activity](#introduction-to-this-activity)
- [Activity 1 Modify the page layout using Bootstrap rows and columns](#activity-1-modify-the-page-structure-using-bootstrap-rows-and-columns)
- [Activity 2 Create a dropdown selector that allows the chart to be changed to display data from a different area of London](#activity-2-create-a-dropdown-selector-to-allow-the-chart-to-be-changed-to-a-different-area)
- [Activity 3 Create a statistics panel that updates when the areas is changed](#activity-3-create-a-statistics-panel-that-updates-when-the-area-is-changed)
- [Activity 4 Add interactivity to the paralympics app](#activity-4-add-interactivity-to-the-paralympics-app)

## Introduction to this activity

So far in the module you have:

- Created the basic structure of a dash app
- Used dash_html_components and dash_core_components to define a static layout in the app.layout
- Used dassh_bootstrap_components CSS to style the dash app
- Created charts using Plotly Express; and possibly using Plotly Go
- Added the charts to a dash app

In this activity you are going to look again at using Bootstrap to modify the app layout; and
[Dash core components](https://dash.plotly.com/dash-core-components) and the callback function decorator for achieving interaction.

This activity uses a simple household waste recycling app. The data is from the [London Datastore](https://data.london.gov.uk).

The charts mimic those displayed in the Environment section of the London Datastore website.

The directory structure of the app is:

```text
/recycle_app/
    recycle_app.py  # Creates the Dash app
    recyclingcharts.py  # Creates the recycling chart 
    recyclingdata.py  # Processes the recycling data and statistics
    /assets/  # Directory for css, images etc
    /data/ # Directory containing the datasets
```

Note: `recyclingcharts.py` and `recyclingdata.py` define classes. This is just to give you an example of using classes rather than functions (paralympics_app uses functions). You do not need to structure your code in classes.

You will need to refer to the [Dash documentation](https://dash.plotly.com/) as this guidance in this document alone will be insufficient to complete the activities.

Have a look at `recycle_app/recycle_app.py` and then run it to see the current app.

## Activity 1: Modify the page structure using Bootstrap rows and columns

Currently, the Dash app has a single full width column layout.

In this activity you will modify the current layout so that it looks like this:

![Dash app layout](/activities/recycle.png)

One of the ways you can define the overall structure with Bootstrap is to divide the page into rows and columns.

Refer to the [dash-bootstrap-components layout documentation](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/layout/) and the section of the page 'Rows with columns'.

Modify the current `app.layout` to a layout with:

- one row and one column for the page main heading
- one row with two columns for the chart and a chart selector and statistics

This will create the structure, though you have not yet moved any of the current page elements into that structure.

The code below indicates how to do this:

```python
app.layout = dbc.Container(fluid=True, children=[
    html.Br(),
    html.H1('Waste and recycling'),
    html.P('Turn London waste into an opportunity – by reducing waste, reusing and recycling more of it.',
           className='lead'),
    html.H2('Recycling'),
    dcc.Graph(id='recycle-chart', figure=fig_rc),


    # First row here
    dbc.Row(dbc.Col(html.P("A single column"))),
    # Second row here
    dbc.Row([
        # This is for the London area selector and the statistics panel.
        dbc.Col(width=3, children=[
            html.P('col 1')
        ]),
        # Add the second column here. This is for the figure.
        dbc.Col(width=9, children=[
            html.P('col 2')
        ]),
    ]),
])
```

When you save the changes to `recycle_app.py` your app should update in the browser. Make sure the app still runs.

Now move the current HTML and chart elements into the row/column structure and deleted the sample text we added in the last step:

- Move `html.H1('Waste and recycling')` and the following `html.P` into the first row and delete `html.P("A single column")`.
- Move `html.H2('Recycling')` and `dcc.Graph(id='recycle-chart', figure=fig_rc)` into the second column of the second row after the `children=` and delete `html.P('col 2')`.

Make sure the app still runs. It should now look like this:

![Dash app layout with rows and cols](/activities/recycle2.png)

This part of the activity has just given you a layout to work with. Next you need to start adding interactivity.

## Activity 2: Create a dropdown selector to allow the chart to be changed to a different area

Currently you see a chart comparing the average rate for all of England to the average rate for London.

Add a drop down selector to 'col1' allow you to choose a different area rather than London.

Remember, the basic steps for the callback function are:

- Define the input
- Define the output
- Write the callback function using the `@callback` decorator

You may need to refer to the [Dash callback documentation](https://dash.plotly.com/basic-callbacks).

### Add the necessary imports

Before creating the first callback you need to import Input and Output.

```python
from dash import html, dcc, Dash, Input, Output
```

### Define the input

The 'input' will be the dropdown selector which does not currently exist in the layout.

Use the [dash core components `dcc.Dropdown()`](https://dash.plotly.com/dash-core-components/dropdown) for this, however to understand its behaviour you need to understand how an HTML `<select>` works so read [an online HTML reference](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select) if you are not familiar with this.

To create the dropdown you will need to define:

- an `id` so that the code can find the element on the page, e.g. `id="area-select"`
- the default `value` to select, in this case 'London'
- a list of the `options`, in this case the areas that be selected

The areas that can be selected can be accessed from the `data` object that is created at the start of the code in `recycle_app.py`. The object has a method `area_list` which is a list of the areas. This is what you will use for the options. The code below iterates the list and generates the options values from it.

The code to create the dropdown selector looks like this:

```python
html.H4("Select Area"),
dcc.Dropdown(id="area-select",
             options=[{"label": x, "value": x} for x in data.area_list],
             value="London"),
```

Add the code to the first column of the second row in the `app.layout` and remove the `html.P('col 1')`.

Check the app still runs. You should be able to select any of the areas. Though we have not yet added the callback function so nothing will happen when you select a different area!

The input is now the 'select area' dropdown which has an `id=area-select` and the property of the dropdown that has the changed area is the `value=`.

### Define the output

When the input, i.e. the area selector created in the last step, changes you want to change the chart. The chart is the 'output'. The chart is defined in the layout as follows:

```python
dcc.Graph(id='recycle-chart', figure=fig_rc)
```

The `id` lets the code find the chart on the page. The `figure` is the property that needs to be updated when the change to the input is made.

### Write the callback function

Callbacks are called on the app and use elements in the layout as their input and output. So the callback functions are defined in a separate section after the app.layout has been created.

The general syntax is:

```python
@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    return f'Output: {input_value}'
```

The `@app.callback` decorator needs to be directly above the callback function declaration. If there is a blank line between the decorator and the function definition, the callback registration will not be successful.

From the previous steps you should know the component id and properties!

```python
@app.callback(
    Output("recycle-chart", "figure"),
    Input("area-select", "value")
    )
```

You can call the function anything you like. It should be meaningful and follow python naming convention. The convention is that the name describes the callback output(s).

The argument you are going pass to the function the area-select value. You can use any name for the function arguments, but you must use the same names inside the callback function as you do
in its definition, just like in a regular Python function. The arguments are positional: first the Input items and then any State items are given in the same order as in the decorator.

Name the function and argument as follows:

```python
@app.callback(
    Output("recycle-chart", "figure"),
    Input("area-select", "value")
    )
def update_recycling_chart(area_select):
```

Now implement the code in the function.

The code should create a recycling chart using the area selected; and then return the updated to the element specified in the output property, ie to the `figure=` property of the chart with `id=recycle-chart`.

To create chart using the area use `rc.create_chart(area_select)`. The `rc` object is defined near the start of `recycle_app.py` using the RecyclingChart class, and `create_chart()` is a function defined in that class.

The full callback now looks like this:

```python
@app.callback(
    Output("recycle-chart", "figure"),
    Input("area-select", "value")
    )
def update_recycling_chart(area_select):
    fig_rc = rc_updated.create_chart(area_select)
    return fig_rc
```

Check that the app still runs. Try and change the area using the selector and the chart should update.

## Activity 3 Create a statistics panel that updates when the area is changed

In this activity you will create a statistics panel using a Bootstrap card layout.

More information on the dash bootstrap components card component is [here](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/card/).

More information on the bootstrap styles used in cards is [here](https://getbootstrap.com/docs/5.3/components/card/).

This activity uses the same input as the previous one. You could therefore update the existing callback to add a second output and modify the function so that it creates and returns both the updated chart and the updated stats panel. However, to keep the code separated for this activity we will create a second callback for the stats panel.

### Define the input

This is the same input as for the chart.

Look at the first column of the second row in the app layout. You should see the dropdown with an `id='area-select'` and the item that is selected from the list is the `value=` parameter.

So, as before, you can reference the country that is selected as `Input("area-select", "value")`.

### Define the output

The output does not currently exist in the app.layout.

Add an html.Div with an id of 'stats-card' below the area selector in the first column of the second row. The stats card will be contained in the Div, that is, it will be defined using the `children=` property of the Div.

The output will be the div with `id='stats-card'` and the property `children=`.

In this example, the HTML to generate the card will be created in the callback function.

### Write the callback function

You already know the general sytntax and the details of the Input and Output so you should be able to create the decorator and name the function.

It should look something like this:

```python
@app.callback(
    Output("stats-card", "children"), 
    Input("area-select", "value")
    )
def render_stats_panel(area_select):
```

The function is a little more complex. You need to:

- generate the [card layout](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/card/) using dash bootstrap components. The classes used for styling are detailed in [Bootstrap documentation](https://getbootstrap.com/docs/5.3/components/card/).
- add the values of the statistics for the chosen area. This is accessed using the 'process_data_for_area(area_name)' method of the 'data' object which is created at the start of `recycle_app.py`.

The code looks like this:

```python
@app.callback(Output("stats-card", "children"), Input("area-select", "value"))
def render_stats_panel(area_select):
    # Get the statistics
    data.process_data_for_area(area_select)
    comp_to_eng = f'{data.compare_to_eng:,.0f}'
    comp_to_prev_year = f'{data.change_area:,.0f}'
    best_period = f'{data.best_period}'
    recycling_rate = f'with recycling rate {data.best_rate:,.0f}%'
    
    # Generate the bootstrap format card with the statistics
    card = dbc.Card(className="bg-dark text-light", children=[
        dbc.CardBody([
            html.H4(area_select, id="card-name", className="card-title"),
            html.Br(),
            html.H6("Compared to England:", className="card-title"),
            html.H4(comp_to_eng, className="card-text text-light"),
            html.Br(),
            html.H6("Compared to previous year:", className="card-title"),
            html.H4(comp_to_prev_year, className="card-text text-light"),
            html.Br(),
            html.H6("Best period:", className="card-title"),
            html.H4(best_period, className="card-text text-light"),
            html.H6(recycling_rate, className="card-title text-light"),
            html.Br()
        ])
    ])
    return card
```

### Extension: merge the two callbacks

Merge the two callbacks so that there is a single callback with one Input and two Outputs that renders the stats panel and updates the chart.

Read the [documentation at this page](https://dash.plotly.com/basic-callbacks) and scroll down to find the 'Dash App With Multiple Outputs' section.

For example:

```python
@app.callback(
    Output("stats-card", "children"),
    Output("recycle-chart", "figure"),
    [Input("area-select", "value")])
def render_stats_chart(area_select):
    # add the code here
    # return the variables in the order the outputs are defined
    return card, fig_rc
```

## Activity 4 Add interactivity to the paralympics app

This activity assumes you have completed the activities 1 to 3 and have gained an understanding of how callbacks are created.

You are given an explanation of what needs to happen, but not the code. You should be able to work out the code yourself.

Use the online references for Dash and Dash Bootstrap Components to help you (links in the previous activities).

Check that you can run `python paralympics_app/paralympics_app.py` before starting.

This builds on the paralympic app. The directory structure of the app is:

```text
/paralympic_app/
    paralympic_app.py  # Creates the dash app
    create_charts.py  # Functions to create the charts for the dash app
    /assets/  # Directory for css, images etc
    /data/ # Directory containing the data files, including geojson
```

### 4.1 Allow the events line chart to be changed to show athletes, nations, events or sports

This activity doesn't tell you to create a column/row layout though you may prefer to do so (see activity 1 for guidance).

#### Create a dropdown selection box

Add a select element to the select the chart type for the first colummn. The Dash component to use
is [dcc.Dropdown](https://dash.plotly.com/dash-core-components/dropdown).

The general syntax is:

```python
dcc.Dropdown(
    id='demo-dropdown',
    options=[
        {'label': 'New York City', 'value': 'NYC'},
        {'label': 'Montreal', 'value': 'MTL'},
        {'label': 'San Francisco', 'value': 'SF'}
    ],
    value='NYC'
),
```

The options are: 'EVENTS', 'SPORTS', 'COUNTRIES', 'PARTICIPANTS'. These correspond to column headings in the dataframe.

Decide on a default, e.g. `value='EVENTS'`.

### Create a callback to update the chart when the selection changes

Before creating the first callback you need to import Input and Output.

```python
from dash import html, dcc, Dash, Input, Output
```

The syntax of a callback is:

```python
@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    return 'Output: {}'.format(input_value)
```

The Output for the callback is the line chart 'id' and the property to update is 'figure'.

The Input for the callback is the dropdown 'id' and the selected
'value'.

The callback function should take the value of the variable selected and pass it to
the `create_charts.line_chart_sports(chart_type)` function to generate the line chart. It should return the new figure (line chart).

### 4.2 Allow users to select whether to display winter or summer for the 'ratio of male and female athletes' chart

Add check boxes so that the person can select whether to see summer, winter or both; then update the charts accordingly.

#### Create the checkboxes for Winter and Summer

To do this you can use the [dcc.Checklist components](https://dash.plotly.com/dash-core-components/checklist).

```python
dcc.Checklist(
    id='mf-ratio-checklist',
    options=[
        {'label': ' Winter', 'value': 'Winter'},
        {'label': ' Summer', 'value': 'Summer'}
    ],
    value=['Winter', 'Summer'],
    labelStyle={"display": "block"},
),
```

### Add the call back

The callback should respond to changes in the checkbox and display or hide the relevant charts.

This time we have two outputs; the two charts. You will need to find the 'ids' of these.

To provide two (or more) outputs e.g.

```python
@app.callback(
    Output("my-id-1", "style"),
    Output("my-id-2", "style"),
    Input("my-checklist", "value"))
```

Rather than changing the 'figure' property, this time you will change the 'style' property to hide/show the figure.

To show or hide an element you can use `style={'display': 'block'}` and `style={'display': 'none'}` on an HTML div.
The 'Div' has been added to the app code for you.

The callback takes the checkbox list of values. The list can contain either or both of Winter and Summer. If neither are
selected the list would be empty.

The callback can check the content of the list of values, and based on the contents, set the style parameters for the
two Outputs.

The callback needs to return two values as a list `[display_val_1, display_val_2]`. The first will affect the first
Output in your list, and the second, the second Output in the list.

The values will be either `style={'display': 'block'}` or `style={'display': 'none'}`.

> There are other charts in the app, try and add an element of interaction to another chart.

## Further practice

A selection of online tutorials for further practice:

- [Creating powerful Pythonic dashboards with Dash - Part 1: Development](https://www.linkedin.com/pulse/creating-powerful-pythonic-dashboards-dash-part-1-russo-%E9%A9%AC%E9%87%8C%E5%A5%A5-)
- [Develop Data Visualization Interfaces in Python With Dash](https://realpython.com/python-dash/)
- [6 Steps to Interactive Python Dashboards with Plotly Dash](https://www.justintodata.com/python-interactive-dashboard-with-plotly-dash-tutorial/)
- [The Dash Callback - Input, Output, State, and more, Charming Data channel, YouTube](https://www.youtube.com/watch?v=mTsZL-VmRVE) This series of video tutorials is well presented and easy to understand.
