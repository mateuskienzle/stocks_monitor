from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

from app import *
from datetime import date

hoje = date.today()

layout=dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle("Cadastro de ativos")),
    dbc.ModalBody([
        dbc.Row([
            dbc.Col([
                dbc.Input(id="nome-ativo", placeholder="Nome")
            ]),
            dbc.Col([
                dbc.Input(id="preco-ativo", placeholder="Preço (R$)")
            ])

        ]),
        dbc.Row([
            dbc.Col(["Data:   ",
                dcc.DatePickerSingle(
                id='my-date-picker-single',
                className='dbc',
                min_date_allowed=date(2005, 1, 1),
                max_date_allowed=date(hoje.year, hoje.month, hoje.day),
                initial_visible_month=date(2017, 8, 5),
                date=date(hoje.year, hoje.month, hoje.day)
                ),
            ]),
            dbc.Col([
                dbc.Input(id="quantidade-ativo", placeholder="Quantidade"),
            ])
        ], style={'margin-top' : '1rem'}),
        dbc.Row([
            dbc.Col([
                html.Img(src="https://petrobras.com.br/sitepetrobras/imgs/bg/logo-social.png", style={'width' : '30%', 'margin-top' : '1rem', 'border-radius' : '15%'})
            ]),
            dbc.Col([
                
            ]),
        ])

    ]),
    dbc.ModalFooter(
        dbc.Row([
            dbc.Col([
                html.Div(id='retorno')
            ]),
            dbc.Col([
                 dbc.Button("Salvar", id="submit-cadastro")       
            ])
        ])

    ),
],id="modal", is_open=False, size='lg')



# Callbacks
@app.callback(
    Output('modal', 'is_open'),
    Output("positioned-toast", "is_open"),
    Input('add-button', 'n_clicks'),
    Input('submit-cadastro', 'n_clicks'),
    State('modal', 'is_open')
)
def func_modal(n1, n2, open):
    if n1 or n2: return [not open, open]
    else: return [open, open]