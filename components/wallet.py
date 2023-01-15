from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

layout = dbc.Row([
    dbc.Col([
        html.Legend("Pagina Wallet")
    ])
])