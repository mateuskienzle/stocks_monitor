from dash import html, dcc
import dash
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from datetime import datetime, date

from app import *
from components import page_inicial, responsive_header, wallet, footer

toast = dbc.Toast("Seu ativo foi cadastrado com sucesso!",
                            id="positioned-toast",
                            header="Confirmação de cadastro",
                            is_open=False,
                            dismissable=False,
                            duration = "4000",
                            icon="success",
                            # top: 66 positions the toast below the navbar
                            style={"position": "fixed", "top": 66, "right": 10, "width": 350})

# Salvar esse df_carteira em um dcc.Store(id=' ', data={}) -> df_carteira.to_dict()
list_trades = [{"date": datetime(2021, 7, 23), 'preco': 123, 'tipo': 'Venda', 'ativo': 'ITUB4', 'vol': 10000, 'logo_url': 'https://logo.clearbit.com/petrobras.com.br', 'valor_total': 'https://logo.clearbit.com/petrobras.com.br'},
                {"date": datetime(2018, 2, 2), 'preco': 123, 'tipo': 'Compra', 'ativo': 'MGLU3', 'vol': 7500, 'logo_url': 'https://logo.clearbit.com/petrobras.com.br', 'valor_total': 'https://logo.clearbit.com/petrobras.com.br' },
                {"date": datetime(2018, 2, 2), 'preco': 123, 'tipo': 'Venda', 'ativo': 'TTEN3', 'vol': 15000, 'logo_url': 'https://logo.clearbit.com/petrobras.com.br', 'valor_total': 'https://logo.clearbit.com/petrobras.com.br' },
                {"date": datetime(2018, 2, 2), 'preco': 123, 'tipo': 'Compra', 'ativo': 'VALE3', 'vol': 29000, 'logo_url': 'https://logo.clearbit.com/petrobras.com.br', 'valor_total': 'https://logo.clearbit.com/petrobras.com.br' },
                {"date": datetime(2018, 2, 2), 'preco': 123, 'tipo': 'Compra', 'ativo': 'LREN3', 'vol': 50000, 'logo_url': 'https://logo.clearbit.com/petrobras.com.br', 'valor_total': 'https://logo.clearbit.com/petrobras.com.br'}]

df_trades = pd.DataFrame(list_trades)

app.layout = dbc.Container(children=[
    dcc.Store(id='book_data_store', data=df_trades.to_dict()),
    dcc.Store(id='historical_data_store', data={}),
    dcc.Interval(id='interval_update', interval=1000*60),
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
                    html.P("CDI: 1%, CDB: 2%, IBOV: 5%, CDI: 1%, CDB: 2%, IBOV: 5%, CDI: 1%, CDB: 2%, IBOV: 5%")
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
@app.callback(
    Output('historical_data_store', 'data'),
    Input('interval_update', 'n_intervals'),
    State('historical_data_store', 'data'),
    State('book_data_store', 'data')
)
def update_yahoo_finance_base(n, historical_data, book_data):
    if historical_data == {}:
        df = pd.DataFrame()
    return {}
        


if __name__ == "__main__":
    app.run_server(debug=True, port=8051)       