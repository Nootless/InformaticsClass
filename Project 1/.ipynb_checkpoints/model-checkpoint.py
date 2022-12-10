import numpy as np
import pickle
import pandas as pd
import sqlite3 as sql
from sklearn.preprocessing import PolynomialFeatures
from matplotlib import pyplot as plot

# 1. connect to object
db = sql.connect('process_values.db')
# 2. create curosr object
cursor = db.cursor()
# execute() -> used to execute command
# commit() -> save changes
# close() -> closes access for cursor
# db.close() -> closes database connection

# find table name ('sensor_data')
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
# print(cursor.fetchall())

# read in data set
data = pd.read_sql_query('SELECT * FROM sensor_data', db)
print(data)
X = data['sensor1']
Y = data['sensor2']
plot.scatter(X,Y)
