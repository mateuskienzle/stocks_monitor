from dash import html, dcc
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from app import *
from components import page_inicial, responsive_header, wallet, footer

toast = dbc.Toast("Seu ativo foi cadastrado com sucesso!",
                            id="positioned-toast",
                            header="Confirmação de cadastro",
                            is_open=False,
                            dismissable=False,
                            duration = "4000",
                            icon="success",
                            # top: 66 positions the toast below the navbar
                            style={"position": "fixed", "top": 66, "right": 10, "width": 350})

app.layout = dbc.Container(children=[
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dcc.Location(id="url"),
                    responsive_header.layout
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Container(id="page-content", fluid=True),
                    toast
                ]),
            ], style={'height' : '100%'}),
            dbc.Row([
                dbc.Col([
                    html.P("CDI: 1%, CDB: 2%, IBOV: 5%, CDI: 1%, CDB: 2%, IBOV: 5%, CDI: 1%, CDB: 2%, IBOV: 5%")
                ], style={"background-color" : 'black', 'color' : 'white', 'font-size' : '1.5em', 'overflow': 'hidden', 'position' : 'fixed', 'left' : '0', 'bottom' : '0', 'height': '1.5em'} )
            ]),
            
        ])
     ])

], fluid=True)

@app.callback(
    Output('page-content', 'children'), 
    Input('url', 'pathname'))

def render_page(pathname):

    if pathname == '/' or pathname == '/main':
        return page_inicial.layout
    
    if pathname == '/wallet':
        return wallet.layout



if __name__ == "__main__":
    app.run_server(debug=True, port=8051)       