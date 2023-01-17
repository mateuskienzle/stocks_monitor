import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from app import *
from components import modal_adicao

ASIMOV_LOGO = "https://asimov.academy/wp-content/uploads/2021/12/logo_dark.png.webp"
card_icon = {
    "fontSize": '200%',
    "margin": "0 0.9rem 0 0.9rem"
}

icon_bar = dbc.Row([
    dbc.Col([
        dbc.Button(id='add-button',
            children=[html.Div(className="fa fa-plus-circle header-icon", style=card_icon)
            ], style={'border-color': 'transparent',  'background-color': 'transparent'}
        ),
    ], xs=4, width={"order": "last"}),
    dbc.Col([
        dbc.Button(id='home-button', href='/',
            children=[html.Div(className="fa fa-home header-icon", style=card_icon)
            ], style={'border-color': 'transparent', 'background-color': 'transparent'}
        ),
    ], xs=4),
    dbc.Col([
        dbc.Button(id='wallet-button', href='/wallet',
            children=[html.Div(className="fa fa-folder-open-o header-icon", style=card_icon)
            ], style={'border-color': 'transparent', 'background-color': 'transparent'}
        ),
    ], xs=4) 
], className="g-0 ms-auto flex-nowrap mt-3 mt-md-0", align="center",)

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button("Search", color="primary", className="ms-2"),
            width="auto",
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

layout = dbc.Navbar(
    dbc.Container([
        modal_adicao.layout,
        html.A(
            dbc.Row([
                    dbc.Col(html.Img(src=ASIMOV_LOGO, height="30px")),
                    dbc.Col(dbc.NavbarBrand("Stocks Monitor", className="ms-2")),
                ], align="center", className="g-0"),
            href="https://asimov.academy", style={"textDecoration": "none"}),
        dbc.NavbarToggler(id="navbar_toggler"),
        dbc.Collapse(
            icon_bar,
            id="navbar_collapse",
            is_open=False,
            navbar=True),
    ]),
    color="dark",
    dark=True,
)

# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar_collapse", "is_open"),
    [Input("navbar_toggler", "n_clicks")],
    [State("navbar_collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

