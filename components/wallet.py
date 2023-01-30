from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import OrderedDict

import pdb

from app import * 


# lista_de_ativos = [{"Data" : "25/01/2023", "Nome" : "ITUB4", "Quantidade" : "10", "Valor unitário" : "R$9,47", "Valor total" : " R$94,70", "id" : 0}]

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
                                                    id={'type': 'delete_event'},
                                                    style={'background-color' : 'transparent', 'border-color' : 'transparent'}
                                                ), 
                            ], md=1, xs=12, style={'text-align' : 'right'})
                        ])
                    ])
                ], class_name=info_do_ativo['class_card'])
            ])
        ], className='g-2 my-auto')

    return new_card


layout = dbc.Container(children=[], id= 'layout_wallet', fluid=True),

@app.callback(
    Output ('layout_wallet', 'children'),
    Input  ('book_data_store', 'data'),
)

def update_wallet(data):
    df = pd.DataFrame(data)

    lista_de_dicts = []
    for row in df.index:
        infos = df.loc[row].to_dict()
        
        #altera nome da classe do card se for compra ou venda
        if infos['tipo'] == 'Compra':
            infos['class_card'] = 'card_compra'
        else:
            infos['class_card'] = 'card_venda'
        infos['id'] = row
        lista_de_dicts.append(infos)
        print(infos)

    lista_de_cards = []
    for dicio in lista_de_dicts:
        card = generate_card(dicio)
        lista_de_cards.append(card)
    
    return lista_de_cards
