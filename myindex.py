from dash import html, dcc
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from app import *
from components import header, page_inicial, wallet


app.layout = dbc.Container(children=[
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dcc.Location(id="url"),
                    header.layout
                ]),
            ],style={'background-color' : "#1c1a35"} ),
            dbc.Row([
                dbc.Col([
                    dbc.Container(id="page-content", fluid=True)
                ]),
            ], style={'background-color' : "#120a19", 'height' : '100%'}),
            
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
    app.run_server(debug=True)       