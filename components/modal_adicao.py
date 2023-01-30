from dash import html, dcc, Input, Output, State, no_update, callback_context
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
from datetime import datetime, date

from app import *
from components.page_inicial import financer
from datetime import date

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
                max_date_allowed=date.today(),
                initial_visible_month=date(2017, 8, 5),
                date=date.today()
                ),
            ], sm=12, md=6),
            dbc.Col([
                dbc.Input(id="quantidade_ativo", placeholder="Quantidade", type='number', min=0, step=1),
            ])
        ], style={'margin-top' : '1rem'}),
        dbc.Row([
            dbc.Col([
                html.Img(id='imagem_ativo', src="https://petrobras.com.br/sitepetrobras/imgs/bg/logo-social.png", style={'width' : '30%', 'margin-top' : '1rem', 'border-radius' : '15%'})
            ]),
            dbc.Col([
                dbc.RadioItems(id='compra_venda_radio', options=[{"label": "Compra", "value": 'Compra'}, {"label": "Venda", "value": 'Venda'}], value='Compra'),
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
# Callback para checar o loading state -----
@app.callback(
    Output('submit_cadastro', 'children'),

    Input('submit_cadastro', 'n_clicks'),
    Input('add_button', 'n_clicks'),
    # Input('positioned_toast', 'icon'),
)
def add_spinner(n, n2):
    trigg_id = callback_context.triggered[0]['prop_id'].split('.')[0]

    if trigg_id == 'submit_cadastro':
        return [dbc.Spinner(size="sm"), "  Carregando informações do ativo..."]
    elif trigg_id == 'add_button':
        return "Salvar"
    else:
        return no_update

# Callback para limpar infos do modal -----
@app.callback(
    Output('nome_ativo', 'value'),
    Output('preco_ativo', 'value'),
    Output('data_ativo', 'date'),
    Output('quantidade_ativo', 'value'),

    Input('positioned_toast', 'header')
)
def reset_data_modal(icon):
    trigg_id = callback_context.triggered[0]['prop_id'].split('.')[0]

    if trigg_id != 'positioned_toast':
        return no_update
    else:
        if "Confirmação" in icon:
            return [None, None, date.today(), None]
        else:
            return no_update
    
# Callback do modal ------------------------
@app.callback(
    Output('modal', 'is_open'),
    Output("positioned_toast", "is_open"),
    Output('positioned_toast', 'header'),
    Output('positioned_toast', 'children'),
    Output('positioned_toast', 'icon'),
    Output('imagem_ativo', 'src'),
    Output('book_data_store', 'data'),

    Input('add_button', 'n_clicks'),
    Input('submit_cadastro', 'n_clicks'),

    State('nome_ativo', 'value'),
    State('modal', 'is_open'),
    State('compra_venda_radio', 'value'),
    State('preco_ativo', 'value'),
    State('data_ativo', 'date'),
    State('quantidade_ativo', 'value'),
    State('book_data_store', 'data')
)
def func_modal(n1, n2, ativo, open, radio, preco, periodo, vol, df_data):
    trigg_id = callback_context.triggered[0]['prop_id'].split('.')[0]
    if trigg_id == '': return no_update
    # print('TIPO:', type(data)) #  <class 'str'>
    # print('DATA:', data) # 2023-01-27
    # print('TIPO:', type(preco)) #  <class 'float'>
    # print('PREÇO:', preco) # 1.44353
    # logo = ''
    return_default = ['', '' , '']
    return_fail_inputs = ['Não foi possível registrar a sua ação!', 
                    'É necessário preencher todos os campos do Formulário.',
                    'primary']
    return_fail_ticker = return_fail_inputs.copy()
    return_fail_ticker[1] = 'É necessário inserir um Ticker válido.'
    return_compra = ['Confirmação de Adição', 'Registro de COMPRA efetivado!', 'success']
    return_venda =  ['Confirmação de Remoção', 'Registro de VENDA efetivado!', 'warning']
    
    # Casos de trigg
    # 1. Botão de abrir modal
    if trigg_id == 'add_button':
        return [not open, open, *return_default, '', df_data]
    
    # 2. Salvando ativo
    elif trigg_id == 'submit_cadastro':  # Corrigir caso de erro - None
        if None in [ativo, preco, vol] and open:
            return [open, not open, *return_fail_inputs, '', df_data]
        else:
            ticker = financer.get_symbol_object(ativo)
            if ticker:
                df = pd.DataFrame(df_data)
                logo = ticker.info['logo_url']
                preco = round(preco, 2)
                df.loc[len(df)] = [periodo, preco, radio, ativo, vol, logo, vol*preco]    
                df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
                df.sort_values(by='date', ascending=False)
                df.to_csv('registro_ativos.csv')
                df_data = df.to_dict()

                retorno = return_compra if radio == 'Compra' else return_venda
                return [not open, open, *retorno, '', df_data]
            else:   
                return [not open, open, *return_fail_ticker, '', df_data]
    # if n1 or n2: return [not open, open, *retorno, '', df_data]
    # else: return [open, open, *retorno, '', df_data]