import logging
import json
import Levenshtein

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/inventory-management', methods=['POST'])
def evaluate():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    target = data[0]['searchItemName'].lower()
    items = data[0]['items']
    items = [i.lower() for i in items]

    for i in items:
        print(Levenshtein.editops(target, i))

    logging.info("My result :{}".format(result))
    return json.dumps(result)



