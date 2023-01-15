from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app import *

height_style={'height': '100%'}

# =========  Layout  =========== #
layout = dbc.Container([
    # Linha 1
    dbc.Row([
        # Card 1
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Dropdown(id='dropdown_card1', multi=True, value='AAPL', options=[{"label": 'MAT', "value": 'MAT'}, {"label": 'AAPL', "value": 'AAPL'}]),
                    dcc.Graph(id='line_graph',) # config={"displayModeBar": False, "showTips": False})
                ])
            ], style=height_style)
        ], xs=12, md=8),
        # Card 2
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Checklist(id='checklist_card2', value=[1], inline=True,
                        options=[{'label': 'moda', 'value': 1}, {'label': 'siderurgica', 'value': 2}]),
                    dcc.Graph(id='radar_graph')
                ])
            ], style=height_style)
        ], xs=12, md=4)
    ], className='g-2 my-auto'),
    # Linha 2
    dbc.Row([
        # Card 3 - card multiplo
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='indicator_graph')
                        ])
                    ], style={'height': '100%'})
                ], xs=6, md=4),
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dcc.Graph(id='line2_graph')
                                ])
                            ], style=height_style)
                        ])
                    ], className='my-auto', style={'height': '50%'}),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dcc.Graph(id='podium_graph')
                                ])
                            ], style=height_style)
                        ])
                    ], className='g-2 my-auto', style={'height': '50%'})
                ], xs=6, md=8)
            ], style=height_style, className='g-2')
        ], xs=12, md=6),
        # Card 4
        dbc.Col([
            dbc.Card([
                dbc.CardBody([

                ])
            ], style={'height': '100%'})
        ], xs=12, md=6)
    ], className='g-2 my-auto')
], fluid=True)



# =========  Callbacks  =========== #
# callback card 1
@app.callback(
    Output('line_graph', 'figure'),
    Input('dropdown_card1', 'value')
)
def func_card1(dropdown):
    print(dropdown)
    return {}

# callback card 2
@app.callback(
    Output('radar_graph', 'figure'),
    Input('checklist_card2', 'value')
)
def func_card2(checklist):
    print(checklist)
    return {}