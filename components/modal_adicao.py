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
                html.Img(id='imagem_ativo', src="https://petrobras.com.br/sitepetrobras/imgs/bg/logo-social.png", style={'width' : '30%', 'margin-top' : '1rem', 'border-radius' : '15%'})
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
    Output('imagem_ativo', 'src'),
    Output('book_data_store', 'data'),

    Input('add_button', 'n_clicks'),
    Input('submit_cadastro', 'n_clicks'),
    Input('nome_ativo', 'value'),

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
    
    # 2. Digitação do nome do ativo
    elif trigg_id == 'nome_ativo':
        if ativo == None or len(ativo) < 5: return no_update
        else:
            ticker = financer.get_symbol_object(ativo)
            try:
                logo = ticker.info['logo_url']
            except:
                logo = ''
            return [open, not open, *return_default, logo, df_data]
    
    # 3. Salvando ativo
    elif trigg_id == 'submit_cadastro':
        if None in [ativo, preco, vol] and open:
            return [open, not open, *return_fail_inputs, '', df_data]
        else:
            ticker = financer.get_symbol_object(ativo)
            if ticker:
                df = pd.DataFrame(df_data)
                periodo = datetime.strptime(periodo, '%Y-%m-%d')
                df.loc[0] = [periodo, preco, radio, ativo, vol, logo, vol*preco]    
                df.sort_values(by='date', ascending=False)
                df.to_csv('registro_ativos.csv')
                df_data = df.to_dict()

                retorno = return_compra if radio == 'c' else return_venda
                return [not open, open, *retorno, '', df_data]
            else:
                return [not open, open, *return_fail_ticker, '', df_data]
    # if n1 or n2: return [not open, open, *retorno, '', df_data]
    # else: return [open, open, *retorno, '', df_data]