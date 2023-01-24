# Creating a multi page Dash app

This is an optional activity for those wanting to create a multi-page app.

You will likely need to refer to the [Multi page apps and URL support](https://dash.plotly.com/urls) in the Dash documentation.

The code for this activity is withing the `multi_page_app` directory.

## File structure for a multi page app

Plotly recommends either:

1. Each app is contained in a separate file (or directory)

```
- app.py
- index.py
- apps
   |-- __init__.py
   |-- app1.py
   |-- app2.py
```

or

2. A flat project layout with callbacks and layouts separated into different files:

```
- app.py
- index.py
- callbacks.py
- layouts.py
```

For this activity we will take the first approach.

In both of these project structures, the Dash instance is defined in a separate app.py, while the entry point for running the app is index.py.

This separation is required to avoid circular imports: the files containing the callback
definitions require access to the Dash app instance however if this were imported from index.py, the initial loading of index.py would ultimately require itself to be already imported, which cannot be satisfied.

### app.py

This file defines the Dash instance.

The dash-bootstrap-component LUX template is used to provide consistent styling for the apps.

### index.py

This file both defines the routing for the app and a layout for the index page (layout is optional).

The routing, i.e. which app to display when a given url is entered, is defined in the `display_page` callback.

`app.layout` provides a sort of template for pages in the app.

### app1/recycle_app.py

The recycle app from first activity has been copied into the directory just to keep the files for each activity
separate.

The recycle_app.py has been changed:

- `app` is now created in app.py and is added as an import
- the previous code to create the `app` in recycle_app.py has been deleted
- the previous code to run the server has been deleted
- the layout is created as `layout=` and not `app.layout=`

### app2

This is a simple Dash app copied from the [Dash documentation sample code](https://github.com/plotly/dash-recipes/tree/master/multi-page-app)

## TASK: Run the multi-page Dash app

1. Open `index.py` and run the code to create app server.
2. Go to [http://127.0.0.1:8050/app1](http://127.0.0.1:8050/app1)
   and you should see the recycle app.
3. Go to [http://127.0.0.1:8050/app2](http://127.0.0.1:8050/app2), and you should see '
   Fruit Selector'.

## TASK: Create a navigation bar

Refer to
the [Dash bootstrap components documentation for nav bar](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/navbar/)
for more options and alternatives.

Using bootstrap styling the following code would create a navbar:

```python
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
```

We don't want to duplicate the navbar code on every page so define the variable `navbar` to create the navbar (see
above) and add this to `index.py` after the imports.

Then add the navbar variable to the `app.layout` in `index.py` in the layout just before the page content.

```python
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])
```

Anything that you add to `app.layout` will be visible on every page. The above places the navbar before the main page
content i.e. at the top of the page.

Stop and restart the app. You should now have a multi-page app with a nav bar.

## TASK: Add a third app

Create a new app called app3.

You can create your own or copy one of
the [sample apps in the Dash repository on GitHub](https://github.com/plotly/dash-sample-apps).

You may need to modify the app code as we did for the recycle app.

Add a link to the `index.py` for app3.

Re-run the app and make sure you can access your third app.
