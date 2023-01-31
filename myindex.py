from dash import html, dcc, no_update
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from datetime import datetime, date
import yfinance as yf

from app import *
from components import page_inicial, responsive_header, wallet, footer

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

# def atualizar_dados(ticker_name):
#     for _ in range(3):
#         ticker = yf.Ticker(ticker_name)

# # Lendo o book de transações
# try:
#     df_book = pd.read_csv('book_data.csv', index_col=0)
# except: 
#     df_book = pd.DataFrame(columns=['date', 'preco', 'tipo', 'ativo', 'vol', 'logo_url', 'valor_total'])

# ativos_na_carteira = list(df_book['ativo'].unique())
# df_book = df_book.to_dict()

# # Lendo os dados históricos ja registrados - atualizando o que for necessário
# try:
#     df_historical_data = pd.read_csv('historical_data.csv', index_col=0)
#     for ativo in ativos_na_carteira:
#         pass
## NOTE CONTINUAR DAQUI - LÓGICA DE REGISTRAR OS ATIVOS!
# except:
#     # Criando o df do formato que queremos
#     columns = pd.MultiIndex.from_product([ativos_na_carteira, ['Date', 'Close']])
#     df_historical_data = pd.DataFrame(columns=columns)


# # Atualizando os dados a partir do df
# df_book = df_book.to_dict()
# df_historical_data = df_historical_data.to_dict()

    


# Salvar esse df_carteira em um dcc.Store(id=' ', data={}) -> df_carteira.to_dict()
list_trades = [{"date": datetime(2021, 7, 23), 'preco': 123, 'tipo': 'Venda', 'ativo': 'ITUB4', 'vol': 10000, 'logo_url': 'https://logo.clearbit.com/itau.com.br', 'valor_total': 'https://logo.clearbit.com/petrobras.com.br'},
                {"date": datetime(2018, 2, 2), 'preco': 123, 'tipo': 'Compra', 'ativo': 'MGLU3', 'vol': 7500, 'logo_url': 'https://logo.clearbit.com/magazineluiza.com.br', 'valor_total': 'https://logo.clearbit.com/petrobras.com.br' },
                {"date": datetime(2018, 2, 2), 'preco': 123, 'tipo': 'Venda', 'ativo': 'TTEN3', 'vol': 15000, 'logo_url': 'https://logo.clearbit.com/ri.3tentos.com.br', 'valor_total': 'https://logo.clearbit.com/petrobras.com.br' },
                {"date": datetime(2018, 2, 2), 'preco': 123, 'tipo': 'Compra', 'ativo': 'VALE3', 'vol': 29000, 'logo_url': 'https://logo.clearbit.com/vale.com.br', 'valor_total': 'https://logo.clearbit.com/petrobras.com.br' },
                {"date": datetime(2018, 2, 2), 'preco': 123, 'tipo': 'Compra', 'ativo': 'LREN3', 'vol': 50000, 'logo_url': 'https://logo.clearbit.com/lojasrenner.com.br', 'valor_total': 'https://logo.clearbit.com/petrobras.com.br'}]
df_trades = pd.DataFrame(list_trades)


toast = dbc.Toast("Seu ativo foi cadastrado com sucesso!",
                            id="positioned_toast",
                            header="Confirmação de cadastro",
                            is_open=False,
                            dismissable=False,
                            duration = "4000",
                            icon="success",
                            style={"position": "fixed", "top": 66, "right": 10, "width": 350})


app.layout = dbc.Container(children=[
    dcc.Store(id='book_data_store', data=df_trades.to_dict()),
    dcc.Store(id='historical_data_store', data={}),
    # dcc.Interval(id='interval_update', interval=1000*60),
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
# Callback pages -------------------
@app.callback(
    Output('page-content', 'children'), 
    Input('url', 'pathname'))

def render_page(pathname):

    if pathname == '/' or pathname == '/main':
        return page_inicial.layout
    
    if pathname == '/wallet':
        return wallet.layout

# Callback pra guardar a data do yfinance
# @app.callback(
#     Output('historical_data_store', 'data'),
#     Input('interval_update', 'n_intervals'),
#     State('historical_data_store', 'data'),
#     State('book_data_store', 'data')
# )
# def update_yahoo_finance_base(n, historical_data, book_data):
#     if historical_data == {}:
#         df = pd.DataFrame()
#     return {}

# Callback para salvar o book_data para CSV
@app.callback(
    Output('div_retorno', 'children'),
    Input('book_data_store', 'data')
)
def book_to_csv(book_data):
    pd.DataFrame(book_data).to_csv('book_data.csv')
    return []



if __name__ == "__main__":
    app.run_server(debug=True, port=8051)  
