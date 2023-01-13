from dash import html, dcc
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from app import *
from components import header, profile, main, wallet





content = html.Div(id="page-content")


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
                    content
                ]),
            ], style={'background-color' : "#120a19", 'height' : '91vh'}),
            
        ])
     ])

], fluid=True)

@app.callback(
    Output('page-content', 'children'), 
    Input('url', 'pathname'))

def render_page(pathname):

    if pathname == '/' or pathname == '/main':
        return main.layout
        
    if pathname == '/profile':
        return profile.layout
    
    if pathname == '/wallet':
        return wallet.layout



if __name__ == "__main__":
    app.run_server(debug=True, port=8051)       