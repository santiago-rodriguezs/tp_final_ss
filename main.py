import soundfile as sf
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for, flash
from flask import send_from_directory
from werkzeug.utils import secure_filename
import os
import numpy as np
from flask import jsonify

UPLOAD_FOLDER = "./"

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.after_request
def add_header(response):
    response.headers['Pragma'] = 'no-cache'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = '0'
    return response

@app.route("/results", methods = ["GET", "POST"])
def results():
    if request.method == 'GET':
        return jsonify(gato=True, hola="rebo")
    elif request.method == 'POST':
        print("entre por post")
        req_data = request.get_json()
        #PROCESAR DATOS
        return print(req_data)
    
# @app.route('/results', methods=['POST']) #GET requests will be blocked
# def results():
#     req_data = request.get_json()

#     harmonics = req_data['harmonics']
#     frequency = req_data['frequency']
#     time = req_data['time']

#     return '''
#            The harms value is: {}
#            The freqs value is: {}
#            The time version is: {}'''.format(harmonics, frequency, time)


if __name__ == "__main__":
        app.run(debug = True, port = 3003)
