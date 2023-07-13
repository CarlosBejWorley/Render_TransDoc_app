from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from dash import html

#Definiendo el elemento alerta para visualizar el nombre del documento que el usuario suba al sistema 
alert = html.Div(
    [
         dbc.Alert(" Upload a document to translate ", color="info", id="doc_alert", is_open=False,style={
             "textAlign": "center",
             "marginLeft": "auto",
             "marginRight": "auto",
         })
    ]
)