from flask import Flask,render_template,url_for,request
import pickle
import numpy as np
import sklearn

myapp = Flask(__name__)

@myapp.route("/")
def home():
    return render_template("index.html")
@myapp.route("/model")
def model():
    return render_template("model.html")
@myapp.route("/predict",methods=["GET","POST"])
def prediction():
    return render_template("output.html")


myapp.run(debug=True,port=8500)
