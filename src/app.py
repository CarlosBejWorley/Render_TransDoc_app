#Importando librerias
import dash
import dash_labs as dl
import dash_bootstrap_components as dbc
from components.navbar.navbar import navbar
from components.form.form import form
from components.doc_alert.doc_alert import alert
import pathlib
from werkzeug.utils import secure_filename
from pdfminer.high_level import extract_text

import base64
import os
from urllib.parse import quote as urlquote
import glob
from docx import Document
from back_functions.CargosAutoTest_Translate import procesar_doc


from flask import Flask, send_from_directory
from dash import dcc, html
from dash.dependencies import Input, Output, State

#Declarando donde se van a alojar los documentos cargados y descargados
UPLOAD_DIRECTORY = "uploaded_files/"
DOWNLOAD_DIRECTORY = "download_files/"

#Funciones para borrar el directorio de archivos al recargar la pagina
delete_files = glob.glob(UPLOAD_DIRECTORY+'*.docx')
delete_files_pdf = glob.glob(UPLOAD_DIRECTORY+'*.pdf')

for f in delete_files:
    os.remove(f)

for f in delete_files_pdf:
    os.remove(f)

def borrar_downloads():
    delete_downloads = glob.glob(DOWNLOAD_DIRECTORY+'*.docx')
    delete_py = glob.glob(DOWNLOAD_DIRECTORY+'*.py')    
    print("Borrando descargas")
    for f in delete_downloads:
        os.remove(f)
        print("Descarga borrada")
    for f in delete_py:
        os.remove(f)    

borrar_downloads()

# Declarando la instancia de dash 
server = Flask(__name__)
app = dash.Dash(server=server, plugins=[dl.plugins.pages], external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server= app.server

@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(DOWNLOAD_DIRECTORY, path, as_attachment=True)

#Creando elementos para agregar a la vista principal
docInfo = alert

format_link=  html.A("You can access the available job formats here", id="format_link", target="_blank",href="https://worleyparsons.sharepoint.com/sites/People_grp/GOF/Global%20Job%20Profiles/Forms/AllItems.aspx?viewid=91cf3383%2D27de%2D4bb9%2D9930%2D69f44f6ec8aa")

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

reload_button = html.Div(
    [
        html.A(
            "Translate another document", id="reload_button", className="d-grid gap-2 col-6 mx-auto", n_clicks=0, href="/"
        ),
        
    ]
)

def translate_file(file_path,discipline,education,experience):
        print("Saving File!!!")
        translated_file=procesar_doc(file_path,discipline,education,experience)
        name=file_path.split('/')
        print(name)
        translated_file.save(DOWNLOAD_DIRECTORY+'Translated-'+name[1])

def translate_text_file(file_path, discipline, education, experience):
    if not allowed_file(file_path):
        print("Invalid file type. Allowed file types are: ", ', '.join(ALLOWED_EXTENSIONS))
        return

    if file_path.lower().endswith(".txt"):
        translated_file = procesar_text_file(file_path, discipline, education, experience)
        name = os.path.basename(file_path)
        translated_file.save(os.path.join(DOWNLOAD_DIRECTORY, 'Translated-' + name.rsplit('.', 1)[0] + '.docx'))
    else:
        translate_file(file_path, discipline, education, experience)

def process_pdf_file(name, content):
    if not allowed_file(name):
        print("Invalid file type. Allowed file types are: ", ', '.join(ALLOWED_EXTENSIONS))
        return

    complete_path = os.path.join(UPLOAD_DIRECTORY, name)
    with open(complete_path, "wb") as fp:
        fp.write(content)

    # Procesar el archivo PDF y guardar el contenido en un archivo .txt
    txt_filename = name.rsplit('.', 1)[0] + ".txt"
    with open(os.path.join(UPLOAD_DIRECTORY, txt_filename), "w", encoding="utf-8") as txt_fp:
        text = extract_text(complete_path)
        txt_fp.write(text)

    return txt_filename



ALLOWED_EXTENSIONS = {'docx', 'pdf', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(name, content, discipline, education, experience):
    if not allowed_file(name):
        print("Invalid file type. Allowed file types are: ", ', '.join(ALLOWED_EXTENSIONS))
        return

    data = content.encode("utf8").split(b";base64,")[1]
    complete_path = os.path.join(UPLOAD_DIRECTORY, name)
    with open(complete_path, "wb") as fp:
        fp.write(base64.decodebytes(data))

    if name.lower().endswith(".pdf"):
        txt_filename = process_pdf_file(name, base64.decodebytes(data))
        translate_text_file(os.path.join(UPLOAD_DIRECTORY, txt_filename), discipline, education, experience)
    elif name.lower().endswith(".docx"):
        translate_file(complete_path, discipline, education, experience)

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

def allowed_file_error_message():
    return html.Div(
        "Invalid file type. Allowed file types are: " + ", ".join(ALLOWED_EXTENSIONS),
        style={
                "color": "#A83B42",
                "background-color" : "#ea868f",
                "border-radius" : ".25rem",
                "padding" : "1rem 1rem",
                "border" : "solid 1px transparent",
                "border-color" : "#F35C75"
            },
        className="text-center"
    )   

#Vista Principal
app.layout = dbc.Container(
    [   navbar,
        dbc.Container([
            dbc.Row(html.H3("Welcome to JDT Bot – Job Description Translator Bot", className="text-center",)),
            dbc.Row(html.H4("Follow these steps:")),
            dbc.Row(html.H5("1. Upload your document to be translated and exported to new format: ")),
            dbc.Row(format_link, style={"textAlign": "center"}),
            dbc.Row(upload),
            dbc.Row(allowed_file_error_message(), id="allowed-file-message"),
            dbc.Row(docInfo),
            dbc.Row(html.H5("2. Define extra content to be added:")),
            dbc.Row(form),
            dbc.Row(html.H5("3. Translate your document:")),
            dbc.Row(button),
            dbc.Row(html.H5("4. Download your Document:")),
            dbc.Row(html.H5(id="download_File", style={"textAlign": "center"})),
            dbc.Row(dbc.Collapse(html.H5(reload_button),id="reload_collapse",is_open=False), className="text-center")
        ]            
        )      
        
    ],
    className="dbc",
    fluid=True,
)

""" Desplegar alerta al subir un documento """
@app.callback(
    [Output("doc_alert", "children"), Output("doc_alert", "is_open"), Output("allowed-file-message", "children")],
    [Input("upload-data", "contents")],
    [State("upload-data", "filename"), State("doc_alert", "is_open")]
)
def update_alert(contents, uploaded_filenames, is_open):
    if not contents:
        return "Upload a document to translate", False, None

    name = uploaded_filenames[0] if uploaded_filenames else None
    content = contents[0] if contents else None

    if not allowed_file(name):
        return "Upload a document to translate", False, allowed_file_error_message()

    if name and is_open is not True:
        return "File: " + name + " processed successfully!", True, None

    return "Upload a document to translate", False, None




"""Guardar el documento subido, traducirlo y generar un nuevo documento descargable"""

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
                save_file(name, data, discipline, education, experience)

        files = uploaded_files()
        if len(files) == 0 :
            return "Load a file on first step to translate"
        else:
            return [file_download_link(files[0])]
            
"""Desplegar opción de nuevo documento"""
@app.callback(
    Output("reload_collapse","is_open"),
    Input("download_File","children")
)
def update_reload(content):
    if content == "Load a file on first step to translate":
        return False
    else:
        return True

"""Opción para traducir un nuevo documento"""
@app.callback(
    Output("reload_button", "children"),
    Input("reload_button","n_clicks")
)
def reset_upload(click):
    if click is not None:
        borrar_downloads()
        return "Translate another document"
    

# Declarando el servidor
if __name__ == "__main__":
    app.run_server(debug=True, host='127.0.0.1')