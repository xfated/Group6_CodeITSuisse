import logging
import json
import math
import numpy as np
import pandas as pd
from io import StringIO
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/pre-tick', methods=['POST'])
def evaluate_tick():                              ## Main Function
    
    # data = request.get_json()
    # logging.info("data sent for evaluation {}".format(data))

    # data = StringIO(data)

    # inputs = data.split('\n')
    # df_list = []
    
    # for i in inputs:
    #     temp_list = []
    #     data = i.split(',')
    #     for j in data:
    #         temp_list.append(int(j))
    #     df_list.append(temp_list)

    data = request.data
    data = data.decode("utf-8") 
    df = pd.read_csv(data,sep=",")
    # columns_names = ['Open','High','Low','Close','Volume']
    # df = pd.Dataframe(df_list, columns=columns_names)

    # df = pd.read_csv(TESTDATA, sep=",", delimiter="\n")

    df1 = df[['Close Price']]

    #Create a variable to predict 'x' days out into the future
    future_days = 1
    #Create a new column (the target or dependent variable) shifted 'x' units/days up
    df1['Prediction'] = df1[['Close Price']].shift(-future_days)

    #Prepare train data
    X = np.array(df1.drop(['Prediction'], 1))[:-future_days]
    y = np.array(df1['Prediction'])[:-future_days]

    #Split dataset
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

    tree = DecisionTreeRegressor().fit(x_train, y_train)
    tree_prediction = tree.predict(x_future)
    price = round(tree_prediction[0],1)

    logging.info("My result:{}".format(price))
    result = {"outputs": price}
    return json.dumps(result) 






