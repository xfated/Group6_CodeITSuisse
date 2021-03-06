import logging
import json
import numpy as np
import math

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/fruitbasket', methods=['POST'])
def evaluate_fruitbasket():
    data = request.get_data()
    data = json.loads(data)
    logging.info("data sent for evaluation {}".format(data))

    estimate = 0
    # Parse data
    for item in data.keys():
        estimate += np.random.randint(1,100) * data[item]

    estimate = int(math.ceil(estimate/100.0))*100
    logging.info("My result :{}".format(estimate))
    result = "{}".format(estimate)
    return result



