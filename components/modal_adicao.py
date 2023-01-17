from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from app import *

# input_styles = {
#     'margin' : '1rem',
#     'width' : '80%'
# }

# modal_styles = {
#     'background-color' : '#1c1a35',
#     'border-color' : 'transparent',
#     'color' : '#e28743'
# }

# modal_button_styles = {
#     'background-color' : '#e28743',
#     'border-color' : '#1c1a35',
#     'color' : '#1c1a35'
# }

input_styles = {}
modal_styles = {}
modal_button_styles = {}

layout=dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle("Cadastro de ativos")),
    dbc.ModalBody([

        dbc.Input(id="nome-ativo", placeholder="Nome", type="text"),
        dbc.Input(id="preco-ativo", placeholder="Preço (R$)", type="text"),
        dbc.Input(id="quantidade-ativo", placeholder="Quantidade", type="number"),
        dbc.Input(id="data-ativo", placeholder="Data", type="text"),
    ]),
    dbc.ModalFooter(
        dbc.Button(
            "Salvar", id="submit-cadastro", n_clicks=0
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
    if n1 or n2: return not open
    else: return open

        