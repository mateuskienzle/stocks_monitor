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
import tinycss2

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

# with open('assets/style.css') as f:
#     css_file = f.read()

# cor_textoTerciario = css_file[-10:-3]
# font_textoTerciario = float(css_file[-29:-26]) + 18.5

INDICATOR_FONT = 35
AXIS_FONT_SIZE = 20
AXIS_COLOR = '#7d9696'


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
        correct_timedelta = pd.Timestamp(correct_timedelta)
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
                                                    html.Legend(str(noticia_ativo['title']), className='textoTerciario')
                                                ]),
                                            ]),
                                            dbc.Row([
                                                dbc.Col([
                                                    html.Legend("Fonte: " + str(noticia_ativo['publisher']), style={'marginTop' : '1rem'}, className='textoTerciario')
                                                ]),
                                            ]),
                                        ], md=10, xs=6),
                                        dbc.Col([
                                            dbc.Card([
                                                dbc.CardBody([
                                                        html.Legend(noticia_ativo['tickerName'], className='textoTerciario')
                                                ], style={'background-color' : '#002b36'})
                                            ])
                                            
                                        ], md=2, xs=12, style={'text-align' : 'center'})
                                    ])
                                ])
                            ], href=noticia_ativo['link'], target='_blank')
                        ], style={'background-color' : 'primary'})
                    ],)
        ], className='g-2 my-auto')
    return new_card

def generate_list_of_news_cards(lista_tags_ativos):
    lista_tags_ativos = list(noticias.keys())
    lista_de_cards_noticias = []
    # logos = {}

    # threads = []
    # for i, tags_ativos in enumerate(lista_tags_ativos):
    #     threads.append(threading.Thread(target=pegar_logo, args=(tags_ativos, logos, i)))
    #     threads[-1].start()

    # for t in threads:
    #     t.join()

    # lista_auxliar = []
    for i, ativo in enumerate(lista_tags_ativos):
        for j, noticia in enumerate(noticias[ativo]):
            # if noticias[ativo][j]['title'] not in lista_auxliar:
            #     lista_auxliar.append(noticias[ativo][j]['title'])
                noticias[ativo][j]['tickerName'] = ativo[:-3]
                # print(noticias[ativo][j])
                # print(noticias[ativo])
                # print(ativo)
                # import pdb
                # pdb.set_trace()
                card_news = generate_card_news(noticias[ativo][j])
                lista_de_cards_noticias.append(card_news)

    random.shuffle(lista_de_cards_noticias,random.random)
    return lista_de_cards_noticias

try:
    df_book_data = pd.read_csv('book_data.csv', index_col=0)
except:
    columns = ['date', 'preco', 'tipo', 'ativo', 'exchange', 'vol', 'logo_url', 'valor_total']
    df_book_data = pd.DataFrame(columns=columns)

df_compra_e_venda = df_book_data.groupby('tipo').sum()



# =========  Layout  =========== #
layout = dbc.Container([
    # Linha 1
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend("Total da carteira", className='textoPrincipal'),
                            html.Legend("R$" + str(df_book_data['valor_total'].sum() - df_compra_e_venda['valor_total']['Venda']), className='textoSecundario')
                        ], style={'text-align' : 'center'})
                    ])
                ])
            ])
        ], md=3),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Legend("CDI", className='textoPrincipal'),
                            html.Legend("13.65%", className='textoSecundario')
                        ], style={'text-align' : 'center'})
                    ])
                ])
            ]),
        ], md=2),

        dbc.Col([
            
        ], md=7,  id= 'cards_valores_ativos')
    ], className='g-2 my-auto'),

    # Linha 2
    dbc.Row([
        # Card 1
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dcc.Dropdown(id='dropdown_card1', className='dbc textoTerciario', value=[], multi=True, options=[]),
                        ], sm=12, md=3),
                        dbc.Col([
                            dbc.RadioItems(
                                options=[{'label': x, 'value': x} for x in PERIOD_OPTIONS],
                                value='1y',
                                id="period_input",
                                inline=True,
                                className='textoTerciario'
                            ),
                        ], sm=12, md=7),
                        dbc.Col([
                            html.Span([
                                    dbc.Label(className='fa fa-percent '),
                                    dbc.Switch(id='profit_switch', value=True, className='d-inline-block ms-1'),
                                    dbc.Label(className='fa fa-money')
                            ], className='textoTerciario'),
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
                            html.Legend('Gestão Setorial IBOV', className='textoSecundario'),
                            dbc.Switch(id='ibov_switch', value=True, label="Comparativo"),
                        ])
                    ], className='textoTerciario'),
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
                        dbc.Row([
                            dbc.Col([
                                html.Legend('Ranking de desempenhos', className='textoSecundario')
                            ])  
                        ]),
                        dbc.Row([
                            dbc.Col([
                                dcc.Graph(id='podium_graph', config={"displayModeBar": False, "showTips": False},  style=HEIGHT)
                            ])
                        ])    
                ])
            ], style=HEIGHT)
        ], xs=6, md=5),
        # Card 5 - asimov news
        dbc.Col([
            
        ], xs=12, md=4, id='asimov_news', style={"height": "100%", "maxHeight": "35rem", "overflow-y": "auto"})
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
    fig.update_xaxes(tickfont=dict(family='Courier', size=AXIS_FONT_SIZE, color=AXIS_COLOR))
    fig.update_yaxes(tickfont=dict(family='Courier', size=AXIS_FONT_SIZE, color=AXIS_COLOR))
    
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
    fig.update_layout(MAIN_CONFIG, showlegend=True, polar=dict(angularaxis = dict(tickfont_size = AXIS_FONT_SIZE, color=AXIS_COLOR)))


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
        title = {"text": f"<br><span style='font-size:{INDICATOR_FONT};'>Evolução Patrimonial<br>Ambos relativos a: {period}</span>"},
        value = df_patrimonio['soma'][-1],
        number = {'prefix': "R$", 'valueformat': '.2s'},
        delta = {'relative': True, 'valueformat': '.1%', 'reference': df_patrimonio['soma'][1]},
        domain = {'row': 0, 'column': 0},
    ))
    fig.add_trace(go.Indicator(
        mode = "number+delta",
        title = {"text": f"<br><span style='font-size:{INDICATOR_FONT};'>Percentual</span>"},
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
    if news != []:
        return no_update
    # if news[0]['props']['children'] != None:
    #     return no_update
    else:
        titulo = dbc.Card([
            dbc.CardBody([
                html.Legend('Notícias ',className='textoSecundario')
            ])
        ])
        return [titulo] + generate_list_of_news_cards(list(noticias.keys())) 
    
#callback podium graph
@app.callback(
    Output('podium_graph', 'figure'),
    Output('cards_valores_ativos', 'children'),
    Input('book_data_store', 'data'),
    Input('period_input', 'value'),
    State('historical_data_store', 'data')
)

def atualizar_podium_graph(book_data, period, historical_data):
    df_book = pd.DataFrame(book_data)
    df_hist = pd.DataFrame(historical_data)

    df_book['datetime'] = pd.to_datetime(df_book['date'], format='%Y-%m-%d %H:%M:%S')

    df2 = df_book.groupby(by=['ativo', 'tipo'])['vol'].sum()

    diferenca_ativos = {}
    for ativo, new_df in df2.groupby(level=0):
        compra, venda = 0, 0
        try:
            compra = new_df.xs((ativo, 'Compra'))
        except: pass
        try:
            venda = new_df.xs((ativo, 'Venda'))
        except: pass
        diferenca_ativos[ativo] = compra - venda

    ativos_existentes = dict((k, v) for k, v in diferenca_ativos.items() if v >= 0)

    if period == 'ytd':
        correct_timedelta = date.today().replace(month=1, day=1)
        correct_timedelta = pd.Timestamp(correct_timedelta)
    else:
        correct_timedelta = date.today() - TIMEDELTAS[period]

    dict_desempenhos = {}
    dict_valores = {}
    for key, value in ativos_existentes.items():
        #atualiza valores para o podium graph
        df_auxiliar = (df_hist[df_hist.symbol.str.contains(key)])
        df_auxiliar['datetime'] = pd.to_datetime(df_auxiliar['datetime'], format='%Y-%m-%d %H:%M:%S')
        df_periodo = df_auxiliar[df_auxiliar['datetime'] > correct_timedelta]
        desempenho_ativo = df_periodo['close'].iloc[-1]/df_periodo['close'].iloc[0]
        dict_desempenhos[key] = desempenho_ativo

        #atualiza cards dos valores dos ativos logo abixo do header
        valor_atual = df_periodo['close'].iloc[-1]
        diferenca_periodo= valor_atual/df_periodo['close'].iloc[0]
        dict_valores[key] = valor_atual, diferenca_periodo
        dfativos= pd.DataFrame(dict_valores).T.rename_axis('ticker').add_prefix('Value').reset_index()
        dfativos['Value1']= dfativos['Value1']*100 - 100

    lista_valores_ativos = []
    seta_crescendo = ['fa fa-arrow-up', 'textoTerciarioPorcentagemUp']
    seta_caindo = ['fa fa-arrow-down', 'textoTerciarioPorcentagemDown']
    for ativo in range(len(dfativos)):
        tag_ativo = dfativos.iloc[ativo][0]
        valor_ativo = dfativos.iloc[ativo][1]
        variacao_ativo = dfativos.iloc[ativo][2]
        if variacao_ativo < 0:
            lista_valores_ativos.append([tag_ativo, valor_ativo, variacao_ativo, seta_caindo[0], seta_caindo[1]])
        else: 
            lista_valores_ativos.append([tag_ativo, valor_ativo, variacao_ativo, seta_crescendo[0], seta_crescendo[1]])

    lista_colunas = []
    if len(lista_valores_ativos) <= 5:
        for i in range(len(lista_valores_ativos)):
            col = dbc.Col([
                        html.Legend(lista_valores_ativos[i][0], className='textoPrincipal'),
                        html.Legend(["R$", lista_valores_ativos[i][1], " ", html.I(className=lista_valores_ativos[i][3]), lista_valores_ativos[i][2].round(2), "%"], className=lista_valores_ativos[i][4])
                ], style={'text-align' : 'center'})
            
            lista_colunas.append(col)
    else: 
        for i in range(5):
            col = dbc.Col([
                        html.Legend(lista_valores_ativos[i][0], className='textoPrincipal'),
                        html.Legend(["R$", lista_valores_ativos[i][1], " ", html.I(className=lista_valores_ativos[i][3]), lista_valores_ativos[i][2].round(2), "%"], className=lista_valores_ativos[i][4])
                ], style={'text-align' : 'center'})
            
            lista_colunas.append(col)



    card_ativos= dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            *lista_colunas
                        ])
                    ],)
                ]),

    ativos = sorted(dict_desempenhos, key=dict_desempenhos.get, reverse=True)[:3]
    podium_dict = {}
    for posicao in range(3):
        dict_desempenhos[ativos[posicao]] = (dict_desempenhos[ativos[posicao]]*100) - 100
        podium_dict[ativos[posicao]] = dict_desempenhos[ativos[posicao]]



    df_podio = pd.DataFrame(list(podium_dict.items()), columns=['Ativos', ' '])
    df_podio.loc[0:1] = [df_podio.loc[1], df_podio.loc[0]]
    fig = px.bar(df_podio, x="Ativos", y=" ")

    range_min = df_podio.loc[2][1].round() -5
    range_max = df_podio.loc[1][1].round() +20

    fig.update_layout(MAIN_CONFIG, yaxis={'ticksuffix': '%', 'range' : [range_min, range_max]})
    fig.update_xaxes(tickfont=dict(family='Courier', size=AXIS_FONT_SIZE, color=AXIS_COLOR))
    fig.update_yaxes(tickfont=dict(family='Courier', size=AXIS_FONT_SIZE, color=AXIS_COLOR))


    fig.add_layout_image(dict(
            source="https://cdn0.iconfinder.com/data/icons/sport-balls/512/silver_medal.png",
            x=0.195,
            y=0.85,
            )
    )
    fig.add_layout_image(
        dict(
            source="https://cdn0.iconfinder.com/data/icons/sport-balls/512/gold_medal.png",
            x=0.525,
            y=0.85,
        ))
    fig.add_layout_image(dict(
            source="https://cdn0.iconfinder.com/data/icons/sport-balls/512/bronze_medal.png",
            x=0.86,
            y=0.85,
            )
    )
    fig.update_layout_images(dict(
            xref="paper",
            yref="paper",
            sizex=0.20,
            sizey=0.15,
            xanchor="right",
            yanchor="bottom"
    ))

    return fig, card_ativos