from dash import html, dcc, Input, Output, State, no_update
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from app import *
from datetime import datetime, date
import numpy as np
import random
from math import log10, floor

import threading

import yfinance as yf
from yfinance_class.y_class import Asimov_finance
from dash_bootstrap_templates import ThemeSwitchAIO
from pandas.tseries.offsets import DateOffset

financer = Asimov_finance()

offsets = [DateOffset(days=5), DateOffset(months=1), DateOffset(months=3), DateOffset(months=6), DateOffset(years=1), DateOffset(years=2)] 
delta_titles = ['5 dias', '1 mês', '3 meses', '6 meses', '1 ano', '2 anos', 'Ano até agora']
PERIOD_OPTIONS = ['5d','1mo','3mo','6mo','1y','2y', 'ytd']

TIMEDELTAS = {x: y for x, y in zip(PERIOD_OPTIONS, offsets)}
TITLES = {x: y for x, y in zip(PERIOD_OPTIONS, delta_titles)}

HEIGHT={'height': '100%'}
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

df_ibov = pd.read_csv('tabela_ibov.csv')

df_ibov['Part. (%)'] = pd.to_numeric(df_ibov['Part. (%)'].str.replace(',','.'))
df_ibov['Qtde. Teórica'] = pd.to_numeric(df_ibov['Qtde. Teórica'].str.replace('.', ''))
df_ibov['Participação'] = df_ibov['Qtde. Teórica'] / df_ibov['Qtde. Teórica'].sum()
df_ibov['Setor'] = df_ibov['Setor'].apply(lambda x: x.split('/')[0].rstrip())
df_ibov['Setor'] = df_ibov['Setor'].apply(lambda x: 'Cons N Cíclico' if x == 'Cons N Ciclico' else x)

tickers = yf.Tickers('PETR4.SA TTEN3.SA LREN3.SA ITUB4.SA MGLU3.SA VALE3.SA')
noticias = tickers.news()

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

url = 'https://www.google.com/search?q={}+icon+logo&tbm=isch&ved=2ahUKEwj8283-zIb9AhX_TbgEHXvGCL0Q2-cCegQIABAA&oq=TTEN3+icon+logo&gs_lcp=CgNpbWcQAzoECCMQJzoGCAAQBxAeOgcIABCABBATOggIABAHEB4QEzoICAAQCBAHEB46BggAEAgQHlDtA1ibDmC7E2gBcAB4AIABiAGIAZEHkgEDMC43mAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=MfDjY7z_Lv-b4dUP-4yj6As&bih=634&biw=1240'
chrome_options = Options()
chrome_options.add_argument("--headless=new")

def formatar_grandes_numeros(num, ends=["", "K", "M", "B", "T"]):
    # divides by 3 to separate into thousands (...000) Divide por 3 os separadores de milhar
	return ends[int(floor(log10(num))/3)]

def definir_evolucao_patrimonial(df_historical_data: pd.DataFrame, df_book_data: pd.DataFrame) -> pd.DataFrame:
    df_historical_data = df_historical_data.set_index('datetime')
    df_historical_data['date'] = df_historical_data.index.date
    df_historical_data = df_historical_data.groupby(['date', 'symbol'])['close'].last().to_frame().reset_index()
    df_historical_data = df_historical_data.pivot(values='close', columns='symbol', index='date')

    df_cotacoes = df_historical_data.copy()
    df_carteira = df_historical_data.copy()

    df_cotacoes = df_cotacoes.replace({0: np.nan}).ffill().fillna(0)
    df_cotacoes.columns = [col.split(':')[-1] for col in df_cotacoes.columns]
    df_carteira.columns = [col.split(':')[-1] for col in df_carteira.columns]
    
    del df_carteira['BVSPX'], df_cotacoes['BVSPX']

    df_book_data['vol'] = df_book_data['vol'] * df_book_data['tipo'].replace({'Compra': 1, 'Venda': -1})
    df_book_data['date'] = pd.to_datetime(df_book_data.date)
    df_book_data.index = df_book_data['date'] 
    df_book_data['date'] = df_book_data.index.date
    
    df_carteira.iloc[:, :] = 0
    for _, row in df_book_data.iterrows():
        df_carteira.loc[df_carteira.index >= row['date'], row['ativo']] += row['vol']
    
    df_patrimonio = df_cotacoes * df_carteira
    df_patrimonio = df_patrimonio.fillna(0)
    df_patrimonio['soma'] = df_patrimonio.sum(axis=1)

    df_ops = df_carteira - df_carteira.shift(1)
    df_ops = df_ops * df_cotacoes
    
    df_patrimonio['evolucao_patrimonial'] = df_patrimonio['soma'].diff() - df_ops.sum(axis=1)           # .plot()
    df_patrimonio['evolucao_percentual'] = (df_patrimonio['evolucao_patrimonial'] / df_patrimonio['soma'])

    ev_total_list = [1]*len(df_patrimonio)
    df_patrimonio['evolucao_percentual'] = df_patrimonio['evolucao_percentual'].fillna(0)
    
    for i, x in enumerate(df_patrimonio['evolucao_percentual'].to_list()[1:]):
        ev_total_list[i+1] = ev_total_list[i] * (1 + x)
        df_patrimonio['evolucao_cum'] = ev_total_list
    
    return df_patrimonio

def slice_df_timedeltas(df: pd.DataFrame, period_string: str) -> pd.DataFrame:
    if period_string == 'ytd':
        correct_timedelta = date.today().replace(month=1, day=1)
    else:
        correct_timedelta = date.today() - TIMEDELTAS[period_string]
    df = df[df.datetime > correct_timedelta].sort_values('datetime')
    return df

def pegar_logo(symbol, logos, count):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url.format(symbol))
    img_div = driver.find_element(By.XPATH, '//*[@id="islrg"]/div[1]/div[1]/a[1]/div[1]/img')
    logos[count] = img_div.get_attribute('src')

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
                                                    html.Legend("Fonte: " + str(noticia_ativo['publisher']), style={"color": 'gray',  'marginTop' : '1rem'})
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
    lista_tags_ativos = list(noticias.keys())
    lista_de_cards_noticias = []
    logos = {}

    threads = []
    for i, tags_ativos in enumerate(lista_tags_ativos):
        threads.append(threading.Thread(target=pegar_logo, args=(tags_ativos, logos, i)))
        threads[-1].start()

    for t in threads:
        t.join()
    
    for i in range(len(lista_tags_ativos)):
        for j in range(len(noticias[lista_tags_ativos[i]])):
            noticias[lista_tags_ativos[i]][j]['tickerLogo'] = logos[i]
            card_news = generate_card_news(noticias[lista_tags_ativos[i]][j])
            lista_de_cards_noticias.append(card_news)

    random.shuffle(lista_de_cards_noticias,random.random)
    return lista_de_cards_noticias


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
                            dcc.Dropdown(id='dropdown_card1', className='dbc', value=[], multi=True, options=[]),
                        ], sm=12, md=3),
                        dbc.Col([
                            dbc.RadioItems(
                                options=[{'label': x, 'value': x} for x in PERIOD_OPTIONS],
                                value='1y',
                                id="period_input",
                                inline=True
                            ),
                        ], sm=12, md=7),
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
                    dbc.Row([
                        dbc.Col([
                            html.Legend('Gestão Setorial IBOV'),
                            dbc.Switch(id='ibov_switch', value=True, label="Comparativo"),
                        ])
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='radar_graph', config={"displayModeBar": False, "showTips": False})
                        ])
                    ])
                ])
            ], style=HEIGHT)
        ], xs=12, md=4)
    ], className='g-2 my-auto'),
    # Linha 2
    dbc.Row([
        # Card 3 - indicator graph
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='indicator_graph', config={"displayModeBar": False, "showTips": False},  style=HEIGHT),
                ])
            ], style=HEIGHT)
        ], xs=6, md=3),
        # Card 4 -podium graph
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='podium_graph', config={"displayModeBar": False, "showTips": False},  style=HEIGHT)
                ])
            ], style=HEIGHT)
        ], xs=6, md=3),
        # Card 5 - asimov news
        dbc.Col([
            dbc.Card([
                dbc.CardBody(id='cardbodytest')
            ], id='asimov_news', style={"height": "100%", "maxHeight": "35rem", "overflow-y": "auto"})
        ], xs=12, md=6)
    ], className='g-2 my-auto')
], fluid=True)



# =========  Callbacks  =========== #
# callback card 1
@app.callback(
    Output('line_graph', 'figure'),
    Input('dropdown_card1', 'value'),
    Input('period_input', 'value'),
    Input('profit_switch', 'value'),
    Input('book_data_store', 'data'),
    State('historical_data_store', 'data')
)
def func_card1(dropdown, period, profit_switch, book_info, historical_info):
    if dropdown == None:
        return no_update
    if type(dropdown) != list: dropdown = [dropdown]
    dropdown = ['BVSPX'] + dropdown
    
    df_hist = pd.DataFrame(historical_info)
    df_hist['datetime'] = pd.to_datetime(df_hist['datetime'], format='%Y-%m-%d %H:%M:%S')
    df_hist = slice_df_timedeltas(df_hist, period)

    fig = go.Figure()

    if profit_switch:
        df_book = pd.DataFrame(book_info)  
        df_patrimonio = definir_evolucao_patrimonial(df_hist, df_book)
        
        fig.add_trace(go.Scatter(x=df_patrimonio.index, y=(df_patrimonio['evolucao_cum']- 1) * 100, mode='lines', name='Evolução Patrimonial'))
    
    else:
        df_hist = df_hist[df_hist['symbol'].str.contains('|'.join(dropdown))]
        for ticker in dropdown:
            df_aux = df_hist[df_hist.symbol.str.contains(ticker)]
            df_aux.dropna(inplace=True)
            df_aux.close = df_aux.close / df_aux.close.iloc[0] - 1
            fig.add_trace(go.Scatter(x=df_aux.datetime, y=df_aux.close*100, mode='lines', name=ticker))
    
    fig.update_layout(MAIN_CONFIG, yaxis={'ticksuffix': '%'})
    return fig

# Callback radar graph
@app.callback(
    Output('radar_graph', 'figure'),
    Input('book_data_store', 'data'),
    Input('ibov_switch', 'value'),
)
def radar_graph(book_data, comparativo):
    df_registros = pd.DataFrame(book_data)
    df_registros['vol'] = abs(df_registros['vol']) * df_registros['tipo'].replace({'Compra': 1, 'Venda': -1})
    
    if comparativo:
        df_provisorio = df_ibov[df_ibov['Código'].isin(df_registros['ativo'].unique())]
        df_provisorio['Participação2'] = df_provisorio['Participação'].apply(lambda x: x*100/df_provisorio['Participação'].sum())

        ibov_setor = df_provisorio.groupby('Setor')['Participação2'].sum()

        df_registros = df_registros[df_registros['ativo'].isin(df_ibov['Código'].unique())]
        df_registros['Participação'] = df_registros['vol'].apply(lambda x: x*100/df_registros['vol'].sum())

        df_registros = df_registros.groupby('ativo')['Participação'].sum()
        df_registros = pd.DataFrame(df_registros).reset_index()
        df_registros['setores'] = np.concatenate([df_provisorio[df_provisorio['Código'] == ativo]['Setor'].values for ativo in df_registros['ativo']])

        df_registros = df_registros.groupby('setores')['Participação'].sum()

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=ibov_setor, theta=ibov_setor.index, name='Distribuição IBOV', fill='toself',
                                    hovertemplate ='<b>IBOV</b>'+'<br><b>Participação</b>: %{r:.2f}%'+ '<br><b>Setor</b>: %{theta}<br>'))
        fig.add_trace(go.Scatterpolar(r=df_registros, theta=df_registros.index, name='Minha Carteira', fill='toself',
                                    hovertemplate ='<b>CARTEIRA</b>'+'<br><b>Participação</b>: %{r:.2f}%'+ '<br><b>Setor</b>: %{theta}<br>'))

    else:
        df_total_ibov = df_ibov.groupby('Setor')['Participação'].sum() * 100
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=df_total_ibov, theta=df_total_ibov.index, name='Distribuição IBOV', fill='toself',
                                    hovertemplate ='<b>IBOV</b>'+'<br><b>Participação</b>: %{r:.2f}%'+ '<br><b>Setor</b>: %{theta}<br>'))

    fig.update_traces(line={'shape': 'spline'})
    fig.update_layout(MAIN_CONFIG, showlegend=True)

    return fig


# callback indicator
@app.callback(
    Output('indicator_graph', 'figure'),
    Input('book_data_store', 'data'),
    Input('period_input', 'value'),
    State('historical_data_store', 'data')
)
def indicator_graph_function(book_data, period, historical_data):
    df_book = pd.DataFrame(book_data)
    df_hist = pd.DataFrame(historical_data)

    df_book['datetime'] = pd.to_datetime(df_book['date'], format='%Y-%m-%d %H:%M:%S')
    # df_book = slice_df_timedeltas(df_book, period)
    df_hist['datetime'] = pd.to_datetime(df_hist['datetime'], format='%Y-%m-%d %H:%M:%S')
    # df_hist = slice_df_timedeltas(df_hist, period)
    
    df_patrimonio = definir_evolucao_patrimonial(df_hist, df_book)
    if period == 'ytd':
        correct_timedelta = date.today().replace(month=1, day=1)
    else:
        correct_timedelta = date.today() - TIMEDELTAS[period]
    df_patrimonio = df_patrimonio[df_patrimonio.index > correct_timedelta].sort_values(by='date')

    period = TITLES[period]

    fig = go.Figure()
    # fig = make_subplots(rows=2, cols=1, vertical_spacing=0.1)

    fig.add_trace(go.Indicator(
        mode = "number+delta",
        title = {"text": f"Evolução Patrimonial<br><span style='font-size:0.8em;color:gray'>Ambos relativos a: {period}</span>"},
        value = df_patrimonio['soma'][-1],
        number = {'prefix': "R$", 'valueformat': '.2s'},
        delta = {'relative': True, 'valueformat': '.1%', 'reference': df_patrimonio['soma'][1]},
        domain = {'row': 0, 'column': 0}
    ))
    fig.add_trace(go.Indicator(
        mode = "number+delta",
        title = {"text": f"Percentual"},
        value = df_patrimonio['evolucao_cum'][-1],
        number = {'suffix': "%", 'valueformat': '.3f'},
        delta = {'relative': True, 'valueformat': '.3%', 'reference': df_patrimonio['evolucao_cum'][1]},
        domain = {'row': 1, 'column': 0}
    ))

    fig.update_layout(MAIN_CONFIG, grid={'rows': 2, 'columns': 1, 'pattern': "independent", 'ygap': 0})
    return fig


# callback para atulizar o dropdown
@app.callback(
    Output('dropdown_card1', 'value'),
    Output('dropdown_card1', 'options'),
    Input('book_data_store', 'data'),
)
def atualizar_dropdown(book):
    df = pd.DataFrame(book)
    unique = df['ativo'].unique()
    
    return [unique[0], [{'label': x, 'value': x} for x in unique]]

# asimov news first initialization
@app.callback(
    Output('asimov_news', 'children'),
    Input('ibov_switch', 'value'),         # input aleatório - necessário no Dash
    State('asimov_news', 'children')
)
def asimov_news_first_initialization(switch, news):
    if news[0]['props']['children'] != None:
        return no_update
    else:
        return generate_list_of_news_cards(list(noticias.keys()))