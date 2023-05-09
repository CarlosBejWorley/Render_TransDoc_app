from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from dash import html

alert = html.Div(
    [
         dbc.Alert("Upload a document to translate", color="primary", id="doc_alert",style={
             "textAlign": "center",
             "marginLeft": "auto",
             "marginRight": "auto",
         })
    ]
)