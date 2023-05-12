from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from dash import html

alert = html.Div(
    [
         dbc.Alert(" Upload a document to translate ", color="info", id="doc_alert", is_open=False,style={
             "textAlign": "center",
             "marginLeft": "auto",
             "marginRight": "auto",
         })
    ]
)