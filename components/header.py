from dash import html, dcc
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from app import *
from components import header, profile, main, wallet

card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 45,
    "margin": "auto",
    "margin-top" : "20px",

}


layout = dbc.Container([
    dbc.Row([
        dbc.Col([
    
            html.H1("Stocks Monitor", style={"color" : "white"}),
            html.H4("ASIMOV", style={"color" : "white"}),
        ], md=3, xs=2, style={"align-content" : "start"}),
        dbc.Col([
            dbc.Button(id='profile-button',
                children=[html.Div(className="fa fa-user", style=card_icon, id='profile-custom')
                ], style={'border-color': 'transparent',  'background-color': 'transparent', 'margin-left' : '10rem'}
            ),
        ], xs=4),
        dbc.Col([
            dbc.Button(id='wallet-button',
                children=[html.Div(className="fa fa-folder-open-o", style=card_icon, id='wallet-custom')
                ], style={'border-color': 'transparent', 'background-color': 'transparent', 'margin-left' : '10rem'}
            ),
        ], xs=4)


        
    ])
], fluid=True)