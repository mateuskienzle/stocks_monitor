from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import OrderedDict



lista_de_ativos = [{"Data" : "25/01/2023", "Nome" : "ITUB4", "Quantidade" : "10", "Valor unitário" : "R$9,47", "Valor total" : " R$94,70", "id" : 0}]


new_card =  dbc.Row([

        dbc.Col([

            dbc.Card([

                dbc.CardBody([

                    dbc.Row([

                        dbc.Col([

                            dbc.Row([

                                dbc.Col([
                                    html.Legend("Nome: " + lista_de_ativos[0]['Nome'])
                                ]),
                            ]),

                            dbc.Row([

                                dbc.Col([
                                    html.Legend("Quantidade: " + lista_de_ativos[0]['Quantidade'])
                                ]),
                            ]),

                            dbc.Row([
                                dbc.Col([
                                    html.Legend("Valor unitário: " + lista_de_ativos[0]['Valor unitário'])
                                ]),
                            ]),

                            dbc.Row([

                                dbc.Col([
                                    html.Legend("Data: " + lista_de_ativos[0]['Data'])
                                ]),

                            ]),

                        ], md=6, xs=6),

                        dbc.Col([
                            dbc.Row([
                                dbc.Col([
                                    html.Img(src="https://petrobras.com.br/sitepetrobras/imgs/bg/logo-social.png", style={'width' : '10%', 'margin-top' : '1rem', 'border-radius' : '15%'}),
                                    html.Legend("Valor total: " + lista_de_ativos[0]['Valor total'])
                                ]),
                            ]),
                        ], md=5, xs=6, style={'text-align' : 'right'}),

                        dbc.Col([
                            dbc.Button([html.I(className = "fa fa-trash header-icon", 
                                                style={'font-size' : '200%'})],
                                                id={'type': 'delete_event','index': lista_de_ativos[0]['id']},
                                                style={'background-color' : 'transparent', 'border-color' : 'transparent'}
                                            ), 
                        ], md=1, xs=12, style={'text-align' : 'right'})
                    ])
                ])
            ])
        ])
    ], className='g-2 my-auto')


layout = dbc.Container([

  new_card,
  new_card,
  new_card,
  new_card,
  new_card

], fluid=True)