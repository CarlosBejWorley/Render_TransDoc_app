import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback, html

discipline_input=dbc.Row(
    [
        dbc.Label("JOB DISCIPLINE:", html_for="discipline-row", width=2),
        dbc.Col(
            dbc.Input(
                type="text", id="discipline-row", placeholder="Enter job discipline"
            ),
            width=10,
        ),
    ],
    className="mb-3",

)

education_input= dbc.Row(
    [
        dbc.Label("REQUIRED EDUCATION:", html_for="education-radios", width=2),
        dbc.Col(
            dbc.RadioItems(
                id="education-radios",
                options=[
                    {"label": "Bachelor", "value": 1},
                    {"label": "Technician", "value": 2},
                    {"label": "Technologist", "value": 3},
                    {"label": "Professional", "value": 4},
                    {"label": "Postgraduated", "value": 5},
                    
                ],
                inline=True,
                labelCheckedClassName="text-primary",
                inputCheckedClassName="border border-primary bg-primary",
            ),
            width="auto",
            
        ),
    ]
)

experience_input= dbc.Row(
    [
        dbc.Label("REQUIRED EXPERIENCE", html_for="experience-radios", width=2),
        dbc.Col(
            dbc.RadioItems(
                id="experience-radios",
                options=[
                    {"label": "Less than a Year", "value": 1},
                    {"label": "1 Year", "value": 2},
                    {"label": "2 Years", "value": 3},
                    {"label": "3 to 5 Years", "value": 4},
                    {"label": "5 to 10 Years", "value": 5},
                    {"label": "10 Years or more", "value": 6},
                ],
                inline=True,
                labelCheckedClassName="text-primary",
                inputCheckedClassName="border border-primary bg-primary",
            ),
            width="auto",
            
        ),
    ], 
)

form = dbc.Container(dbc.Form([discipline_input, education_input, experience_input]),id="container")