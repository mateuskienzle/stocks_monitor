from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import OrderedDict

from app import * 


lista_de_ativos = [{"Data" : "25/01/2023", "Nome" : "ITUB4", "Quantidade" : "10", "Valor unitário" : "R$9,47", "Valor total" : " R$94,70", "id" : 0}]

def generate_card(info_do_ativo):
    new_card =  dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.Row([
                                    dbc.Col([
                                        html.Legend("Nome: " + info_do_ativo['ativo'])
                                    ]),
                                ]),
                                dbc.Row([

                                    dbc.Col([
                                        html.Legend("Quantidade: " + str(info_do_ativo['vol']))
                                    ]),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        html.Legend("Valor unitário: " + str(info_do_ativo['preco']))
                                    ]),
                                ]),
                                dbc.Row([
                                    dbc.Col([
                                        html.Legend("Data: " + info_do_ativo['date'].strftime('%Y-%m-%d'))
                                    ]),
                                ]),
                            ], md=6, xs=6),
                            dbc.Col([
                                dbc.Row([
                                    dbc.Col([
                                        html.Img(src=info_do_ativo['logo_url'], style={'width' : '10%', 'margin-top' : '1rem', 'border-radius' : '15%'}),
                                        html.Legend("Valor total: " + info_do_ativo['preco']*info_do_ativo['vol'])
                                    ]),
                                ]),
                            ], md=5, xs=6, style={'text-align' : 'right'}),
                            dbc.Col([
                                dbc.Button([html.I(className = "fa fa-trash header-icon", 
                                                    style={'font-size' : '200%'})],
                                                    id={'type': 'delete_event','index': lista_de_ativos['id']},
                                                    style={'background-color' : 'transparent', 'border-color' : 'transparent'}
                                                ), 
                            ], md=1, xs=12, style={'text-align' : 'right'})
                        ])
                    ])
                ])
            ])
        ], className='g-2 my-auto')

    return new_card


layout = dbc.Container(children=[], id= 'layout_wallet', fluid=True)

@app.callback(
    Output ('layout_wallet', 'children'),
    Input  ('book_data_store', 'data'),
)

def update_wallet(data):
    df = pd.DataFrame(data)

    lista_de_dicts = []
    for row in df.index:
        infos = df.loc[row].to_dict()
        lista_de_dicts.append(infos)

    lista_de_cards = []
    for dicio in lista_de_dicts:
        card = generate_card(dicio)
        lista_de_cards.append(card)
    
    return lista_de_cards
