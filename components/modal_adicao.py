from dash import html, dcc, Input, Output, State, no_update, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

from app import *
from components.page_inicial import financer
from datetime import date

hoje = date.today()

layout=dbc.Modal([
    dbc.ModalHeader(dbc.ModalTitle("Cadastro de ativos")),
    dbc.ModalBody([
        dbc.Row([
            dbc.Col([
                dbc.Input(id="nome_ativo", placeholder="Nome", type='text')
            ]),
            dbc.Col([
                dbc.Input(id="preco_ativo", placeholder="Preço (R$)", type='number', min=0, step=0.01)
            ])

        ]),
        dbc.Row([
            dbc.Col([
                "Data:   ",
                dcc.DatePickerSingle(
                id='data_ativo',
                className='dbc',
                min_date_allowed=date(2005, 1, 1),
                max_date_allowed=date(hoje.year, hoje.month, hoje.day),
                initial_visible_month=date(2017, 8, 5),
                date=date(hoje.year, hoje.month, hoje.day)
                ),
            ], sm=12, md=6),
            dbc.Col([
                dbc.Input(id="quantidade_ativo", placeholder="Quantidade", type='number', min=0, step=1),
            ])
        ], style={'margin-top' : '1rem'}),
        dbc.Row([
            dbc.Col([
                html.Img(src="https://petrobras.com.br/sitepetrobras/imgs/bg/logo-social.png", style={'width' : '30%', 'margin-top' : '1rem', 'border-radius' : '15%'})
            ]),
            dbc.Col([
                dbc.RadioItems(id='compra_venda_radio', options=[{"label": "Compra", "value": 'c'}, {"label": "Venda", "value": 'v'}], value='c'),
            ]),
        ])
    ]),
    dbc.ModalFooter(
        dbc.Row([
            dbc.Col([dbc.Button("Salvar", id="submit_cadastro")])
        ])

    ),
],id="modal", is_open=False, size='lg')



# Callbacks =======================
# Callback do modal ---------------
@app.callback(
    Output('modal', 'is_open'),
    Output("positioned-toast", "is_open"),
    Output('positioned-toast', 'header'),
    Output('positioned-toast', 'children'),
    Output('positioned-toast', 'icon'),
    Input('add_button', 'n_clicks'),
    Input('submit_cadastro', 'n_clicks'),
    Input('nome_ativo', 'value'),
    State('modal', 'is_open'),
    State('compra_venda_radio', 'value'),
    State('preco_ativo', 'value'),
    State('data_ativo', 'date'),
    State('quantidade_ativo', 'value'),
)
def func_modal(n1, n2, ativo, open, radio, preco, data, quantidade):
    trigg_id = callback_context.triggered[0]['prop_id'].split('.')[0]
    if trigg_id == '': return no_update
    
    print(trigg_id)

    return_fail_inputs = ['Não foi possível registrar a sua ação!', 
                    'É necessário preencher todos os campos do Formulário.',
                    'primary']
    return_fail_ticker = return_fail_inputs.copy()
    return_fail_ticker[1] = 'É necessário inserir um Ticker válido.'
    return_compra = ['Confirmação de Adição', 'Registro de COMPRA efetivado!', 'success']
    return_venda =  ['Confirmação de Remoção', 'Registro de VENDA efetivado!', 'warning']
    
    if trigg_id == 'add_button':
        return [not open, open, *return_fail_inputs]
    else:
        if trigg_id == 'nome_ativo' and ativo != None:
            ticker = financer.get_symbol_object(ativo)
            ticker.info['logo_url'] 
        if None in [ativo, preco, quantidade, data] and open:
            print('caiu aqui')
            return [not open, open, *return_fail_inputs]

        ticker = financer.get_symbol_object(ativo)
        if not ticker:
            print('ativo inexistente')
            return no_update
    
    retorno = return_compra if radio == 'c' else return_venda

    dicio = {'a': ativo, 'b': preco, 'c': data, 'd': quantidade}
    print('DATA:', dicio, 'TIPO DATE:', type(dicio['c']))
    
    if n1 or n2: return [not open, open, *retorno]
    else: return [open, open, *retorno]