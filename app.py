from flask import Flask, make_response, request, render_template
from processxml import readxml, writexml
from dataframe import create_dataframe, create_previous
from generate import model, debug_gen
from viz import generate_json
from sklearn.preprocessing import LabelEncoder
import xml.etree.cElementTree as ET
from dotenv import load_dotenv
import smtplib
import base64
import sys
import os

load_dotenv()

app = Flask(__name__, static_url_path="", static_folder="static")
app.secret_key = os.getenv("SECRET")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template("index.html")
    debug = False
    content_encoded = request.form.get("content")
    param = int(request.form.get("param"))
    length = int(request.form.get("length"))
    content = base64.b64decode(content_encoded)
    root = ET.fromstring(content)
    column_chord = []
    column_step = []
    column_alter = []
    column_octave = []
    column_type = []
    column_dot = []
    readxml(root, column_chord, column_step, column_alter, column_octave, column_type, column_dot)
    data = create_dataframe(column_chord, column_step, column_alter, column_octave, column_type, column_dot)
    enc = LabelEncoder()
    data['note'] = enc.fit_transform(data['note'])
    df = create_previous(data)
    gen_notes = model(df, n_notes=length, param=param)
    if debug:
        gen_notes = debug_gen(data)
    output = writexml(root, data, gen_notes)
    return base64.b64encode(output)

if __name__ == "__main__":
    app.run()