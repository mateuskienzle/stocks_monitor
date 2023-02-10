from dash import html, dcc, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app import *
from datetime import datetime, date
import pdb

import yfinance as yf
from yfinance_class.y_class import Asimov_finance
from dash_bootstrap_templates import ThemeSwitchAIO
from pandas.tseries.offsets import DateOffset

financer = Asimov_finance()

HEIGHT={'height': '100%'}
PERIOD_OPTIONS = ['5d','1mo','3mo','6mo','1y','2y', 'ytd']
MAIN_CONFIG = {
    "hovermode": "x unified",
    "legend": {"yanchor":"top", 
                "y":0.9, 
                "xanchor":"left",
                "x":0.1,
                "title": {"text": None},
                "font" :{"color":"white"},
                "bgcolor": "rgba(0,0,0,0.5)"},
    "margin": {"l":0, "r":0, "t":10, "b":0}
}

# Salvar esse df_carteira em um dcc.Store(id=' ', data={}) -> df_carteira.to_dict()
list_trades = [{"date": datetime(2021, 7, 23), 'tipo': 'Compra', 'ativo': 'ITUB4', 'vol': 10000},
                {"date": datetime(2018, 2, 2), 'tipo': 'Compra', 'ativo': 'MGLU3', 'vol': 7500 },
                {"date": datetime(2018, 2, 2), 'tipo': 'Compra', 'ativo': 'TTEN3', 'vol': 15000 },
                {"date": datetime(2018, 2, 2), 'tipo': 'Compra', 'ativo': 'VALE3', 'vol': 29000 },
                {"date": datetime(2018, 2, 2), 'tipo': 'Compra', 'ativo': 'LREN3', 'vol': 50000 }]

df_trades = pd.DataFrame(list_trades)


# df_book = pd.read_csv('book_data.csv', index_col=0)
# df_ativos_unique = df_book['ativo'].unique()

tickers = yf.Tickers('PETR4.SA TTEN3.SA LREN3.SA ITUB4.SA MGLU3.SA VALE3.SA')
noticias = tickers.news()

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

url = 'https://www.google.com/search?q={}+icon+logo&tbm=isch&ved=2ahUKEwj8283-zIb9AhX_TbgEHXvGCL0Q2-cCegQIABAA&oq=TTEN3+icon+logo&gs_lcp=CgNpbWcQAzoECCMQJzoGCAAQBxAeOgcIABCABBATOggIABAHEB4QEzoICAAQCBAHEB46BggAEAgQHlDtA1ibDmC7E2gBcAB4AIABiAGIAZEHkgEDMC43mAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=MfDjY7z_Lv-b4dUP-4yj6As&bih=634&biw=1240'

def pegar_logo(symbol):
  chrome_options = Options()
  chrome_options.add_argument("--headless")
  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
  driver.get(url.format(symbol))
  
  img_div = driver.find_element(By.XPATH, '//*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img')
  return img_div.get_attribute('src')


def generate_card_news(noticia_ativo):
    new_card =  dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dcc.Link([
                                dbc.CardBody([
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Row([
                                                dbc.Col([
                                                    html.Legend(str(noticia_ativo['title']), style={"color": 'white'})
                                                ]),
                                            ]),
                                            dbc.Row([
                                                dbc.Col([
                                                    html.Legend(str(noticia_ativo['publisher']), style={"color": 'gray', "fontSize": '95%', 'marginTop' : '1rem'})
                                                ]),
                                            ]),
                                        ], md=10, xs=6),
                                        dbc.Col([
                                            html.Img(src=noticia_ativo['tickerLogo'], style={'width' : '50%', 'border-radius' : '15%'})
                                        ], md=2, xs=12, style={'text-align' : 'right'})
                                    ])
                                ])
                            ], href=noticia_ativo['link'], target='_blank')
                        ], style={'background-color' : '#000000'})
                    ],)
        ], className='g-2 my-auto')
    return new_card

def generate_list_of_news_cards(lista_tags_ativos):
    lista_de_cards_noticias = []
    for i in range(len(lista_tags_ativos)):
        logo = pegar_logo(lista_tags_ativos[i])
        for j in range(len(noticias[lista_tags_ativos[i]])):
            noticias[lista_tags_ativos[i]][j]['tickerLogo'] = logo
            card_news = generate_card_news(noticias[lista_tags_ativos[i]][j])
            lista_de_cards_noticias.append(card_news)
    return lista_de_cards_noticias


cards_news = generate_list_of_news_cards(list(noticias.keys()))

# =========  Layout  =========== #
layout = dbc.Container([
    # Linha 1
    dbc.Row([
        # Card 1
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dcc.Dropdown(id='dropdown_card1', className='dbc', value=df_trades['ativo'].unique()[0], multi=True, options=[{'label': x, 'value': x} for x in df_trades['ativo'].unique()]),
                        ], sm=12, md=2),
                        dbc.Col([
                            dbc.RadioItems(
                                options=[{'label': x, 'value': x} for x in PERIOD_OPTIONS],
                                value='1y',
                                id="period_input",
                                inline=True
                            ),
                        ], sm=12, md=8),
                        dbc.Col([
                            html.Span([
                                    dbc.Label(className='fa fa-percent'),
                                    dbc.Switch(id='profit_switch', value=True, className='d-inline-block ms-1'),
                                    dbc.Label(className='fa fa-money')
                            ]),
                        ], sm=12, md=2)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='line_graph', config={"displayModeBar": False, "showTips": False}, style=HEIGHT)    
                        ])
                    ])
                    
                ])
            ], style=HEIGHT)
        ], xs=12, md=8),
        # Card 2
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Checklist(id='checklist_card2', value=[1], inline=True,
                        options=[{'label': 'moda', 'value': 1}, {'label': 'siderurgica', 'value': 2}],persistence=True, persistence_type="session"),
                    dcc.Graph(id='radar_graph', config={"displayModeBar": False, "showTips": False})
                ])
            ], style=HEIGHT)
        ], xs=12, md=4)
    ], className='g-2 my-auto'),
    # Linha 2
    dbc.Row([
        # Card 3 - card multiplo
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='indicator_graph', config={"displayModeBar": False, "showTips": False})
                        ])
                    ], style={'height': '100%'})
                ], xs=6, md=4),
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dcc.Graph(id='line2_graph', config={"displayModeBar": False, "showTips": False})
                                ])
                            ], style=HEIGHT)
                        ])
                    ], className='my-auto', style={'height': '50%'}),
                    dbc.Row([
                        dbc.Col([
                            dbc.Card([
                                dbc.CardBody([
                                    dcc.Graph(id='podium_graph', config={"displayModeBar": False, "showTips": False})
                                ])
                            ], style=HEIGHT)
                        ])
                    ], className='g-2 my-auto', style={'height': '50%'})
                ], xs=6, md=8)
            ], style=HEIGHT, className='g-2')
        ], xs=12, md=6),
        # Card 4
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    *cards_news
                ])
            ], id='asimov_news', style={"height": "100%", "maxHeight": '61em', "overflow-y": "auto"})
        ], xs=12, md=6)
    ], className='g-2 my-auto')
], fluid=True)



# =========  Callbacks  =========== #
# callback card 1
@app.callback(
    Output('line_graph', 'figure'),
    Input('dropdown_card1', 'value'),
    Input('period_input', 'value'),
    State('historical_data_store', 'data')
)
def func_card1(dropdown, period, teste123):
    if dropdown == None:
        return no_update
    if type(dropdown) != list: dropdown = [dropdown]
    dropdown = ['BVSPX'] + dropdown

    df = pd.DataFrame(teste123)
    df = df[df.symbol.str.contains('|'.join(dropdown))]
    df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d %H:%M:%S')

    timedeltas = {'5d': DateOffset(days=5), '1mo': DateOffset(months=1), 
                '3mo': DateOffset(months=3), '6mo': DateOffset(months=6),
                '1y': DateOffset(years=1), '2y': DateOffset(years=2)}

    if period == 'ytd':
        correct_timedelta = date.today().replace(month=1, day=1)
    else:
        correct_timedelta = date.today() - timedeltas[period]

    df = df[df.datetime > correct_timedelta]
    
    df.sort_values(by='datetime', inplace=True)

    fig = go.Figure()
    for ticker in dropdown:
        df_aux = df[df.symbol.str.contains(ticker)]
        df_aux.dropna(inplace=True)
        df_aux.close = df_aux.close / df_aux.close.iloc[0] - 1
        fig.add_trace(go.Scatter(x=df_aux.datetime, y=df_aux.close*100, mode='lines', name=ticker))
        
    fig.update_layout(MAIN_CONFIG, yaxis={'ticksuffix': '%'})
    return fig



    return {} # REMOVER - TESTE
    

    if dropdown == None:
        return no_update
    if type(dropdown) != list: dropdown = [dropdown]
    dropdown = ['^BVSP'] + dropdown
    
    df_joined = pd.DataFrame()
    for ticker in dropdown:
        df = financer.get_symbol_object(ticker).history(period=period, interval='1d')[['Close']]
        df_joined = df_joined.join(df.rename(columns={"Close": ticker}), how='outer')
    
    df_joined.dropna(inplace=True)
    df_retorno = df_joined / df_joined.iloc[0] - 1

    # Tipo 1 de gráfico - Ação x IBOV (RAW) ==============
    # df_retorno = df_retorno.cumsum()

    fig = go.Figure()
    for ticker in dropdown:
        fig.add_trace(go.Scatter(x=df_retorno.index, y=df_retorno[ticker]*100, mode='lines', name=ticker, line_shape='spline'))

    fig.update_layout(MAIN_CONFIG, yaxis={'ticksuffix': '%'})

    return fig

# callback card 2
@app.callback(
    Output('radar_graph', 'figure'),
    Input('checklist_card2', 'value')
)
def func_card2(checklist):
    '''
    Pegar todos os ticks e a sua representação no df. Na sequencia, ponderar essas representações a partir dos setores utilzando o código que foi comentado aqui abaixo
    '''
    data = []
    quant = 200

    # for tick in checklist:
    #     if tick.info == None: continue
    #     data.append({'Setor': tick.info['sector'], 'Quantidade': quant})
    #     quant += quant*1/4
    # df = pd.DataFrame(data)

    # fig = go.Figure()
    # fig.add_trace(go.Scatterpolar(r=df['Quantidade']/100, theta=df['Setor'], fill='toself', name='Minha Carteira'))
    # fig.update_layout(height=500)
    # fig.add_annotation(text=f'Distribuição da carteira relativo à BVSP/setor',
    #     xref="paper", yref="paper",
    #     font=dict(
    #         family="Courier New, monospace",
    #         size=20,
    #         color="#ffffff"),
    #     align="center", bgcolor="rgba(0,0,0,0.5)", opacity=0.8,
    #     x=0.9, y=0.1, showarrow=False)


    return {}

# callback card asimov news
# @app.callback(
#     Output('asimov_news', 'children'),
#     Input('checklist_card2', 'data')
# )
# def func_card2(checklist):
#     print(checklist)
#     return {}


# @app.callback(
#     Output('asimov_news_card_noticia', 'children'),
#     Input('book_data_store', 'data')
# )
# def update_news(data):
#     lista_de_cards_noticias = []
#     # df_book = pd.read_csv('book_data.csv', index_col=0)
#     # df_ativos_unique = df_book['ativo'].unique()
#     # print('noticias aqui')
#     # print('-------------------')
#     for k, v in datastore['ativo'].items():
#         lista_tags_ativos = v
#         lista_de_cards_noticias = generate_list_of_news_cards(df_ativos_unique)
#     return lista_de_cards_noticias

