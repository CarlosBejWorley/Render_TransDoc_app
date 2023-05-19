#libraries
import dash
import dash_labs as dl
import dash_bootstrap_components as dbc
from components.navbar.navbar import navbar
from components.form.form import form
from components.doc_alert.doc_alert import alert

import base64
import os
from urllib.parse import quote as urlquote
import glob
from docx import Document
from back_functions.CargosAutoTest_Translate import procesar_doc


from flask import Flask, send_from_directory
from dash import dcc, html
from dash.dependencies import Input, Output, State

#establishing upload and download files
UPLOAD_DIRECTORY = "uploaded_files/"
DOWNLOAD_DIRECTORY = "download_files/"

#Funciones para borrar el directorio de archivos al recargar la pagina
delete_files = glob.glob(UPLOAD_DIRECTORY+'*.docx')
for f in delete_files:
    os.remove(f)

delete_downloads = glob.glob(DOWNLOAD_DIRECTORY+'*.docx')
for f in delete_downloads:
    os.remove(f)

# Dash instance declaration 
server = Flask(__name__)
app = dash.Dash(server=server, plugins=[dl.plugins.pages], external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server= app.server

@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(DOWNLOAD_DIRECTORY, path, as_attachment=True)

#Creando elementos para agregar a la vista principal
docInfo = alert

format_link=  html.A("You can access the available job formats here", id="format_link", target="",href="https://worleyparsons.sharepoint.com/sites/People_grp/GOF/Global%20Job%20Profiles/Forms/AllItems.aspx?viewid=91cf3383%2D27de%2D4bb9%2D9930%2D69f44f6ec8aa")

upload =   dcc.Upload(
            id="upload-data",
            children=html.Div(
                ["Drag and drop or click to select a file to upload."]
            ),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            multiple=True,
        )

button = html.Div(
    [
        dbc.Button(
            "Translate Document", id="translate-button", className="d-grid gap-2 col-6 mx-auto", n_clicks=0
        ),
        
    ]
)

def translate_file(file_path,discipline,education,experience):
        print("Saving File!!!")
        translated_file=procesar_doc(file_path,discipline,education,experience)
        name=file_path.split('/')
        print(name)
        translated_file.save(DOWNLOAD_DIRECTORY+'translated-'+name[1])

def save_file(name, content,discipline,education,experience):

    #print(content)
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    #print(data)
    complete_path=os.path.join(UPLOAD_DIRECTORY, name)
    with open(complete_path, "wb") as fp:        
        fp.write(base64.decodebytes(data))
    fp.close()

    translate_file(complete_path,discipline,education,experience)

def uploaded_files():
    """List the files in the download directory."""
    files = []
    for filename in os.listdir(DOWNLOAD_DIRECTORY):
        path = os.path.join(DOWNLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files

def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)

#Main layout
app.layout = dbc.Container(
    [   navbar,
        dbc.Container([
            dbc.Row(html.H3("Welcome to JDT Bot – Job Description Translator Bot", className="text-center",)),
            dbc.Row(html.H4("Follow these steps:")),
            dbc.Row(html.H5("1. Upload your document to be translated and exported to new format: ")),
            dbc.Row(format_link, style={"textAlign": "center"}),
            dbc.Row(upload),
            dbc.Row(docInfo),
            dbc.Row(html.H5("2. Define extra content to be added:")),
            dbc.Row(form),
            dbc.Row(html.H5("3. Translate your document:")),
            dbc.Row(button),
            dbc.Row(html.H5("4. Download your Document:")),
            dbc.Row(html.H5(id="download_File", style={"textAlign": "center"}))
        ]            
        )      
        
    ],
    className="dbc",
    fluid=True,
)

""" Toggle uploaded doc info alert """
@app.callback(
    [Output("doc_alert","children"),Output("doc_alert","is_open")],
    Input("upload-data","contents"),
    [State("upload-data","filename"),State("doc_alert","is_open")]
    
)
def update_alert(content,uploaded_filenames,is_open):

    if uploaded_filenames is not None and is_open != True :

        return "File: " + uploaded_filenames[0] + " processed succesfully!", True
    
    elif uploaded_filenames is not None and is_open == True:

        return "File: " + uploaded_filenames[0] + " processed succesfully!", True
    
    return ("Upload a document to translate ", False)


"""Save uploaded file, transalate and regenerate the downloable file."""

@app.callback(
    Output("download_File", "children"),
    [Input("translate-button", "n_clicks")],
    [State("upload-data", "filename"),State("upload-data", "contents"),State("discipline-row", "value"),State("education-radios", "value"),State("experience-radios", "value")]
    #,Input("upload-data", "filename"), Input("upload-data", "contents")
)
def update_output(click,uploaded_filenames, uploaded_file_contents,discipline,education,experience):
    
    if click is not None:

        if uploaded_filenames is not None and uploaded_file_contents is not None:
            for name, data in zip(uploaded_filenames, uploaded_file_contents):
                save_file(name, data,discipline,education,experience)

        files = uploaded_files()
        if len(files) == 0:
            return "Load a file on first step to translate"
        else:
            return [file_download_link(files[0])]

# Testing server
if __name__ == "__main__":
    app.run_server(debug=True, host='127.0.0.1')