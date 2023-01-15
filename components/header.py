from dash import html, dcc
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from app import *
from components import header, page_inicial, wallet, modal_adicao

card_icon = {
    "fontSize": '300%',
    "margin-top" : "50%",
}

# card_icon = {}
layout = dbc.Row([
        dbc.Col([
            modal_adicao.layout,
            dbc.Row([
                dbc.Col([
                    html.Div(className="fa fa-line-chart", style={'color': '#e28743'}),
                ], xs=3, md=2, style={'fontSize': '400%'}),
                dbc.Col([
                    dbc.Row([
                        html.Legend("Stocks Monitor", style={"color" : "white", 'margin-bottom': 0}),
                    ], className='g-3 my-auto'),
                    dbc.Row([
                        html.Legend("ASIMOV", style={"color" : "white", 'margin-top': 0}),
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

# Callback open modal
@app.callback(
    Output('modal_add', 'is_open'),
    Input('add-button', 'n_clicks'),
    State('modal_add', 'is_open')
)
def func_modal(n, open):
    if n: return not open
    else: return open

# 