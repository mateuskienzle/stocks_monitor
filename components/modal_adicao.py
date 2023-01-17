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

        ]),
    
    dbc.Input(id="nome-ativo", placeholder="Nome", style={'width': '30%'}),
    dbc.Input(id="preco-ativo", placeholder="Preço (R$)"),
    dcc.DatePickerSingle(
        id='my-date-picker-single',
        className='dbc',
        min_date_allowed=date(2005, 1, 1),
        max_date_allowed=date(hoje.year, hoje.month, hoje.day),
        initial_visible_month=date(2017, 8, 5),
        date=date(hoje.year, hoje.month, hoje.day)
    ),
    dbc.Input(id="quantidade-ativo", placeholder="Quantidade"),
    html.Div(id='retorno')
    ]),
    dbc.ModalFooter(
        dbc.Button("Salvar", id="submit-cadastro")
    ),
],id="modal", is_open=False, size='lg')

# layout=dbc.Modal([
#     dbc.ModalHeader(dbc.ModalTitle("Cadastro de ativos")),
#     dbc.ModalBody([

#         dbc.Input(id="nome-ativo", placeholder="Nome"),
#         dbc.Input(id="preco-ativo", placeholder="Preço (R$)"),
#         dbc.Input(id="quantidade-ativo", placeholder="Quantidade"),
#         dbc.Input(id="data-ativo", placeholder="Data"),
#     ]),
#     dbc.ModalFooter(
#         dbc.Button("Salvar", id="submit-cadastro")
#     ),
# ], id='modal_add', is_open=False, size='lg', style={'opacity': '0.95'})


# Callbacks
@app.callback(
    Output('modal', 'is_open'),
    Input('add-button', 'n_clicks'),
    Input('submit-cadastro', 'n_clicks'),
    State('modal', 'is_open')
)
def func_modal(n1, n2, open):
    if n1: return not open
    if n2: 
        return not open
    else: return open

# @app.callback(
#     Output('retorno', 'children'),
#     Output('retorno', 'style'),
#     Input('submit-cadastro', 'n_clicks')
# )
# def func_retorno(n):
#     print(n)
#     if n:
#         return ["Registrada ação x", {'color': 'green'}]
#     else:
#         return [None, {}]
        