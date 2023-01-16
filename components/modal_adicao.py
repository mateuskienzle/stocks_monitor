from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

input_styles = {
    'margin' : '1rem',
    'width' : '80%'
}

modal_styles = {
    'background-color' : '#1c1a35',
    'border-color' : 'transparent',
    'color' : '#e28743'
}

modal_button_styles = {
    'background-color' : '#e28743',
    'border-color' : '#1c1a35',
    'color' : '#1c1a35'
}

layout=dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle("Cadastro de ativos"), style={'background-color' : '#1c1a35', 'border-color' : '#e28743','color' : '#e28743'}),
    dbc.ModalBody([

        dbc.Input(id="nome-ativo", placeholder="Nome", type="text", style= input_styles),
        dbc.Input(id="preco-ativo", placeholder="Preço (R$)", type="text", style= input_styles),
        dbc.Input(id="quantidade-ativo", placeholder="Quantidade", type="number", style= input_styles),
        dbc.Input(id="data-ativo", placeholder="Data", type="text", style= input_styles),
    ], style=modal_styles),
    dbc.ModalFooter(
        dbc.Button(
            "Salvar", id="submit-cadastro", n_clicks=0, style=modal_button_styles
        ), style=modal_styles
    ),
], id='modal_add', is_open=False, size='lg')





        