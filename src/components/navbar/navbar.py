import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, html


logo = "assets/worley_logo.png"



navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        html.Img(src=logo, height="50px"),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            
        ]
    ),
    id="principal_navbar"
    
)


