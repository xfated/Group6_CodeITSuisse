import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/fruitbasket', methods=['POST'])
def evaluate_fruitbasket():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    print(data)
    result = { "result": "idk bro"}
    logging.info("My result :{}".format(result))
    return json.dumps(result)


