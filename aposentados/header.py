from dash import html, dcc
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from app import *
from components import modal_adicao

card_icon = {
    "fontSize": '300%',
    "margin-top" : "50%",
}

layout = dbc.Row([
        dbc.Col([
            modal_adicao.layout,
            dbc.Row([
                dbc.Col([
                    html.Div(className="fa fa-line-chart")
                ], xs=3, md=2, style={'fontSize': '400%'}),
                dbc.Col([
                    dbc.Row([
                        html.Legend("Stocks Monitor", style={'margin-bottom': 0}),
                    ], className='g-3 my-auto'),
                    dbc.Row([
                        html.Legend("ASIMOV", style={'margin-top': 0}),
                    ], className='g-3 my-auto')
                ], xs=9, md=10)
            ])
        ], xs=12, md=3),
        dbc.Col([
            dbc.Row([
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
            ])
        ], xs=12, md=2)
    ], justify="between")

