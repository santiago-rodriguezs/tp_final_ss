from flask import Flask
from flask import render_template
from flask import request
from fourier import pulseMainFunction, sincMainFunction

import forms

app = Flask(__name__)

@app.after_request
def add_header(response):
    response.headers['Pragma'] = 'no-cache'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = '0'
    return response

@app.route("/", methods = ["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/seegibbs", methods = ["GET"])
def gibbs():
    return render_template("gibbs.html")


@app.route("/continuous", methods = ["GET", "POST"])
def continuous():
    signalForm = forms.SignalForm(request.form)
    flag = False

    return render_template("continuous.html", flag = flag, form = signalForm)

@app.route("/pulses", methods = ["GET", "POST"])
def pulses():
    signalForm = forms.SignalForm(request.form)
    flag = False

    return render_template("pulses.html", flag = flag, form = signalForm)

@app.route("/results", methods = ["GET","POST"])
def results():
    signalForm = forms.SignalForm(request.form)
    value = ""
    result = ""
    if request.method == "POST":
        t = signalForm.time.data
        freq = signalForm.frequency.data
        method = signalForm.method.data
        value = signalForm.value.data
        c = signalForm.continuous.data

        if (c == "c"):
            result = sincMainFunction(t, freq, method, value)
        else:
            result = pulseMainFunction(t, freq, method, value)
        
    return render_template("results.html", result = result)

@app.route("/about", methods = ["GET"])
def about():
	return render_template("about.html")

if __name__ == "__main__":
        app.run(debug = True, port = 3001)
