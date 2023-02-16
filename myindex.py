from dash import html, dcc, no_update, callback_context
import dash
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from datetime import datetime, date
import yfinance as yf
from tvDatafeed import TvDatafeed, Interval

from app import *
from components.page_inicial import financer
from components import page_inicial, responsive_header, wallet


# PRIMEIRA INICIALIZAÇÃO =========================
'''
Aqui deveremos carregar a nossa base temporal de dados, para que seja possível
diminuir a quantidade de requisições feitas ao yfinance, visto que ele apresenta
instabilidade com certa frequência.
1º - Checar quais são os nossos dados no book_data.csv, se é que o CSV ja existe.
    Retornar aqui quais são os nossos ativos únicos
2º - Checar se todos os ativos presentes na lista retornada acima estão com os
dados em dia. Pra isso utilizar a função df.index.max() pra retornar a data mais
recente de cada ativo. Na sequência fazer as requisições necessárias pro yfinance
3
** Remember:
    - Ler o book_data.csv e historical_data.csv na inicialização!
    - Cirar um dcc.Interval() para atualizar o historical_data.csv se necessário!
'''

# Funções =======================================
def iterar_sobre_df_book(df_book_var: pd.DataFrame, ativos_org_var={}) -> dict:
    for _, row in df_book_var.iterrows():
        if not any(row['ativo'] in sublist for sublist in ativos_org_var):  
            ativos_org_var[row["ativo"]] = row['exchange']
    
    ativos_org_var['BVSPX'] = 'VANTAGE'
    return ativos_org_var 

def atualizar_historical_data(df_historical_var: pd.DataFrame, ativos_org_var={}) -> pd.DataFrame:
    tv = TvDatafeed()
    for symb_dict in ativos_org_var.items():
        new_line = tv.get_hist(*symb_dict, n_bars=5000)[['symbol','close']].reset_index()
        df_historical_var = pd.concat([df_historical_var, new_line], ignore_index=True)

    return df_historical_var.drop_duplicates(ignore_index=True)
    

# Checando se o book de transações existe
ativos_org = {}
try:    # caso exista, ler infos
    df_book = pd.read_csv('book_data.csv', index_col=0)
    ativos_org = iterar_sobre_df_book(df_book)
except: # caso não exista, criar df
    df_book = pd.DataFrame(columns=['date', 'preco', 'tipo', 'ativo', 'exchange', 'vol', 'logo_url', 'valor_total'])

''' Lendo os dados históricos dos ativos ja registrados (e verificando se esse arquivo ja não existe)
Sempre que quiser acessar o histórico de qualquer ativo, utilizar:
    df_historical_data[df_historical_data.symbol == 'ativo']
'''
try:
    df_historical_data = pd.read_csv('historical_data.csv', index_col=0)
except:
    columns = ['datetime', 'symbol', 'close']
    df_historical_data = pd.DataFrame(columns=columns)

df_historical_data = atualizar_historical_data(df_historical_data, ativos_org)

df_book = df_book.to_dict() 
df_historical_data = df_historical_data.to_dict()


toast = dbc.Toast("Seu ativo foi cadastrado com sucesso!",
                            id="positioned_toast",
                            header="Confirmação de cadastro",
                            is_open=False,
                            dismissable=False,
                            duration = "4000",
                            icon="success",
                            style={"position": "fixed", "top": 66, "right": 10, "width": 350})

def generate_card(info_do_ativo):
    new_card =  dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.Row([
                                    dbc.Col([
                                        html.Legend([html.I(className='fa fa-list-alt', style={"fontSize": '85%'})," Nome: " + str(info_do_ativo['ativo'])])
                                    ]),
                                ]),
                                dbc.Row([

                                    dbc.Col([
                                        html.Legend([html.I(className='fa fa-database', style={"fontSize": '85%'})," Quantidade: " + str(info_do_ativo['vol'])])
                                    ]),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        html.Legend([html.I(className='fa fa-usd', style={"fontSize": '100%'}), " Valor unitário: R$" + '{:,.2f}'.format(info_do_ativo['preco'])])
                                    ]),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        html.Legend([html.I(className='fa  fa-calendar', style={"fontSize": '85%'}), " Data: " + info_do_ativo['date'][:10]])
                                    ]),
                                ]),
                            ], md=6, xs=6),
                            dbc.Col([
                                dbc.Row([
                                    dbc.Col([
                                        html.Img(src=info_do_ativo['logo_url'], style={'width' : '10%', 'margin-top' : '1rem', 'border-radius' : '15%'}),
                                        html.Legend([html.I(className='fa fa-handshake-o', style={"fontSize": '100%'}), " Tipo: " + str(info_do_ativo['tipo'])]),
                                        html.Legend([html.I(className='fa fa-usd', style={"fontSize": '100%'}), " Total: R$" + '{:,.2f}'.format(info_do_ativo['preco']*info_do_ativo['vol'])])
                                    ]),
                                ]),
                            ], md=5, xs=6, style={'text-align' : 'right'}),
                            dbc.Col([
                                dbc.Button([html.I(className = "fa fa-trash header-icon", 
                                                    style={'font-size' : '200%'})],
                                                    id={'type': 'delete_event', 'index': info_do_ativo['id']},
                                                    style={'background-color' : 'transparent', 'border-color' : 'transparent'}
                                                ), 
                            ], md=1, xs=12, style={'text-align' : 'right'})
                        ])
                    ])
                ], class_name=info_do_ativo['class_card'])
            ])
        ], className='g-2 my-auto')

    return new_card

app.layout = dbc.Container(children=[
    dcc.Store(id='book_data_store', data=df_book, storage_type='session'),
    dcc.Store(id='historical_data_store', data=df_historical_data, storage_type='session'),
    dcc.Store(id='layout_data', data=[], storage_type='session'),
    dcc.Interval(id='interval_update', interval=1000*600),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dcc.Location(id="url"),
                    responsive_header.layout
                ]),
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Container(id="page-content", fluid=True),
                    toast
                ]),
            ], style={'height' : '100%'}),
            dbc.Row([
                dbc.Col([
                    html.P("CDI: 1%, CDB: 2%, IBOV: 5%, CDI: 1%, CDB: 2%, IBOV: 5%, CDI: 1%, CDB: 2%, IBOV: 5%"),
                    html.Div(id="div_retorno", style={'display':'none'})
                ], style={"background-color" : 'black', 'color' : 'white', 'font-size' : '1.5em', 'overflow': 'hidden', 'position' : 'fixed', 'left' : '0', 'bottom' : '0', 'height': '1.5em'} )
            ]),
            
        ])
     ])

], fluid=True)

# =========  Callbacks  =========== #
# Callback pages
@app.callback(
    Output('page-content', 'children'), 
    Input('url', 'pathname'))

def render_page(pathname):

    if pathname == '/' or pathname == '/main':
        return page_inicial.layout
    
    if pathname == '/wallet':
        return wallet.layout


# Callback para atualizar as databases
@app.callback(
    Output('historical_data_store', 'data'),
    Input('interval_update', 'n_intervals'),
    Input('book_data_store', 'data'),
    State('historical_data_store', 'data')
)
def atualizar_databases(n, book_data, historical_data):
    df_book = pd.DataFrame(book_data)
    df_historical = pd.DataFrame(historical_data)

    ativos = iterar_sobre_df_book(df_book)
    # import pdb; pdb.set_trace()
    df_historical = atualizar_historical_data(df_historical, ativos)

    # atualizando os CSV's
    df_book.to_csv('book_data.csv')
    df_historical.to_csv('historical_data.csv')

    return df_historical.to_dict()


if __name__ == "__main__":
    app.run_server(debug=True, port=8051)  





















# @app.callback(
#     Output('modal', 'is_open'),
#     Output("positioned_toast", "is_open"),
#     Output('positioned_toast', 'header'),
#     Output('positioned_toast', 'children'),
#     Output('positioned_toast', 'icon'),
#     Output('imagem_ativo', 'src'),
#     Output('book_data_store', 'data'),

#     Output('layout_wallet', 'children'),

#     Input('add_button', 'n_clicks'),
#     Input('submit_cadastro', 'n_clicks'),

#     Input('book_data_store', 'data'),
#     Input({'type': 'delete_event', 'index': ALL}, 'n_clicks'),

#     State('nome_ativo', 'value'),
#     State('modal', 'is_open'),
#     State('compra_venda_radio', 'value'),
#     State('preco_ativo', 'value'),
#     State('data_ativo', 'date'),
#     State('quantidade_ativo', 'value'),
#     State('book_data_store', 'data'), 
# )
# def func_modal(n1, n2, data, event, ativo, open, radio, preco, periodo, vol, df_data):
#     trigg_id = callback_context.triggered[0]['prop_id'].split('.')[0]

#     if trigg_id == '': return no_update
#     # print('TIPO:', type(data)) #  <class 'str'>
#     # print('DATA:', data) # 2023-01-27
#     # print('TIPO:', type(preco)) #  <class 'float'>
#     # print('PREÇO:', preco) # 1.44353
#     # logo = ''
#     return_default = ['', '' , '']
#     return_fail_inputs = ['Não foi possível registrar a sua ação!', 
#                     'É necessário preencher todos os campos do Formulário.',
#                     'primary']
#     return_fail_ticker = return_fail_inputs.copy()
#     return_fail_ticker[1] = 'É necessário inserir um Ticker válido.'
#     return_compra = ['Confirmação de Adição', 'Registro de COMPRA efetivado!', 'success']
#     return_venda =  ['Confirmação de Remoção', 'Registro de VENDA efetivado!', 'warning']
    
#     # Casos de trigg
#     # 1. Botão de abrir modal
#     if trigg_id == 'add_button':
#         return [not open, open, *return_default, '', df_data, lista_de_cards]
    
#     # 2. Salvando ativo
#     elif trigg_id == 'submit_cadastro':  # Corrigir caso de erro - None
#         if None in [ativo, preco, vol] and open:
#             return [open, not open, *return_fail_inputs, '', df_data, lista_de_cards]
#         else:
#             ticker = financer.get_symbol_object(ativo)
#             if ticker:
#                 df = pd.DataFrame(df_data)
#                 logo = ticker.info['logo_url']
#                 preco = round(preco, 2)
#                 df.loc[len(df)] = [periodo, preco, radio, ativo, vol, logo, vol*preco]    
#                 df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
#                 df.sort_values(by='date', ascending=False)
#                 df.to_csv('registro_ativos.csv')
#                 df_data = df.to_dict()

#                 retorno = return_compra if radio == 'Compra' else return_venda
#                 return [not open, open, *retorno, '', df_data, lista_de_cards]
#             else:   
#                 return [not open, open, *return_fail_ticker, '', df_data, lista_de_cards]
#     # if n1 or n2: return [not open, open, *retorno, '', df_data]

#     # else: return [open, open, *retorno, '', df_data]
#     elif type(trigg_id) == dict: 
#         if trigg_id == 'delete_event':
#             if trigg_id['index'] == row:
#                 df.drop([trigg_id['index']], axis=0, inplace=True)
#                 return [not open, open, *retorno, '', df_data, lista_de_cards]

#     df = pd.DataFrame(data)

#     lista_de_dicts = []

#     # print('\n\n',event)
#     print('\n\n',trigg_id)
#     for row in df.index:
#         infos = df.loc[row].to_dict()
#         #altera nome da classe do card se for compra ou venda
#         if infos['tipo'] == 'Compra':
#             infos['class_card'] = 'card_compra'
#         else:
#             infos['class_card'] = 'card_venda'
#         infos['id'] = row
#         lista_de_dicts.append(infos)
#         # print(infos)
    
#     # pdb.set_trace()

#     lista_de_cards = []
#     for dicio in lista_de_dicts:
#         card = generate_card(dicio)
#         lista_de_cards.append(card)

#     return [not open, open, *retorno, '', df_data, lista_de_cards]