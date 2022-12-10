import sklearn
import numpy as np
import pickle
import pandas as pd
import sqlite3 as sql
import matplotlib.pyplot as plot

from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from flask import Flask, render_template, url_for, request, redirect
from math import sqrt

myapp = Flask(__name__)


@myapp.route("/", methods=['GET', 'POST'])
def home():
    return render_template("home.html")


@myapp.route("/model", methods=["GET", "POST"])
def model():
    print(request.form['password'])
    if request.method == 'POST':

        if request.form['password'] == 'password':
            # 1. connect to object
            db = sql.connect('process_values.db')
            # 2. create curosr object
            cursor = db.cursor()
            # read in data set
            data = pd.read_sql_query('SELECT * FROM sensor_data', db)
            # print(data)
            X = data['sensor1']
            Y = data['sensor2']
            X = X.values.reshape(-1, 1)
            Y = Y.values.reshape(-1, 1)

            # create polynomial feature
            poly = PolynomialFeatures(degree=3, include_bias=False)
            X_poly = poly.fit_transform(X)
            X_poly = pd.DataFrame(X_poly, columns=['feature1', 'feature1sqd', 'feature1cub'])

            reg = LinearRegression().fit(X_poly, Y)
            prediction = reg.predict(X_poly)
            rmse = sqrt(mean_squared_error(Y, prediction))
            with open('model.pkl', 'wb') as file:
                pickle.dump(reg,file)

            return render_template("model.html", rmse=rmse)

    return redirect(url_for('home'))


@myapp.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        # open model and gather value
        sensor1 = float(request.form.get("sensor"))
        sensor1val = np.array(sensor1)
        with open('model.pkl', 'rb') as file:
            model = pickle.load(file)
    
        # create polynomialfeatures + prediction
        poly = PolynomialFeatures(degree=3, include_bias=False)
        sensor1val = poly.fit_transform(sensor1val.reshape(-1,1))
        sensor1val = pd.DataFrame(sensor1val,columns=['feature1','feature1sqd','feature1cub'])
        prediction = model.predict(sensor1val)[0][0]

        # add to sql database
        data = pd.DataFrame([[sensor1, prediction]], columns=['sensor1','sensor2'])
        con = sql.connect("process_values.db")
        data.to_sql('sensor_data',con,if_exists='append',index=False)
        con.commit()
        con.close()
    
        return render_template("output.html", prediction=prediction, sensor=sensor1)
    return redirect(url_for('home'))


myapp.run(debug=True, port=8500)
