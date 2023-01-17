from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from app import *

layout=dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle("Cadastro de ativos")),
    dbc.ModalBody([

        dbc.Input(id="nome-ativo", placeholder="Nome"),
        dbc.Input(id="preco-ativo", placeholder="Preço (R$)"),
        dbc.Input(id="quantidade-ativo", placeholder="Quantidade"),
        dbc.Input(id="data-ativo", placeholder="Data"),
    ]),
    dbc.ModalFooter(
        dbc.Button(
            "Salvar", id="submit-cadastro"
        )
    ),
], id='modal_add', is_open=False, size='lg', style={'opacity': '0.95'})


# Callbacks
@app.callback(
    Output('modal_add', 'is_open'),
    Input('add-button', 'n_clicks'),
    Input('submit-cadastro', 'n_clicks'),
    State('modal_add', 'is_open')
)
def func_modal(n1, n2, open):
    if n1: return not open
    if n2: return not open
    else: return open

        