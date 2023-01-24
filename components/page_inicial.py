from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app import *
from datetime import datetime, date

import yfinance as yf

HEIGHT={'height': '100%'}
PERIOD_OPTIONS = ['5d','1mo','3mo','6mo','1y','2y','5y','10y','ytd']
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
fake_data = [['PETR4.SA', 23, 323, datetime(2017, 1, 1).date()], ['ITUB4.SA', 23, 323, datetime(2017, 1, 1).date()], ['TTEN3.SA', 23, 323, datetime(2017, 1, 1).date()]]
df_carteira = pd.DataFrame(columns=['nome', 'preço', 'quantidade', 'data'])

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
                            dcc.Dropdown(id='dropdown_card1', className='dbc', value='PETR4.SA', options=[{"label": 'PETR4.SA', "value": 'PETR4.SA'}, {"label": 'ITUB4.SA', "value": 'ITUB4.SA'}, {"label": "TTEN3.SA", "value": "TTEN3.SA"}]),
                        ], sm=12, md=3),
                        dbc.Col([
                            dbc.RadioItems(
                                options=[{'label': x, 'value': x} for x in PERIOD_OPTIONS],
                                value='3mo',
                                id="period_input",
                                inline=True
                            ),
                        ], sm=12, md=9)
                    ]),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='line_graph', config={"displayModeBar": False, "showTips": False})    
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

                ])
            ], style={'height': '100%'})
        ], xs=12, md=6)
    ], className='g-2 my-auto')
], fluid=True)



# =========  Callbacks  =========== #
# callback card 1
@app.callback(
    Output('line_graph', 'figure'),
    Input('dropdown_card1', 'value'),
    Input('period_input', 'value')
)
def func_card1(dropdown, period):
    bov = yf.Ticker('^BVSP')
    ticker = yf.Ticker(dropdown)
    data_ibovespa = bov.history(period=period, interval='1d')['Close']
    data_ticker = ticker.history(period=period, interval='1d')['Close']

    data_ibovespa = data_ibovespa.pct_change()*100
    data_ticker = data_ticker.pct_change()*100

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data_ibovespa.index, y=data_ibovespa.values, name='BVSP', mode='lines', line_shape='spline'))
    fig.add_trace(go.Scatter(x=data_ticker.index, y=data_ticker.values, name=dropdown, mode='lines', line_shape='spline'))

    fig.update_layout(MAIN_CONFIG, height=250, yaxis={'ticksuffix': '%'})
    fig.add_annotation(text=f'Variação em % - BVSP x {dropdown}',
        xref="paper", yref="paper",
        font=dict(
            family="Courier New, monospace",
            size=20,
            color="#ffffff"),
        align="center", bgcolor="rgba(0,0,0,0.5)", opacity=0.8,
        x=0.9, y=0.1, showarrow=False)
    return fig

# callback card 2
@app.callback(
    Output('radar_graph', 'figure'),
    Input('checklist_card2', 'value')
)
def func_card2(checklist):
    print(checklist)
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