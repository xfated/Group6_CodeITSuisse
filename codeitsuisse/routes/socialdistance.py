import logging
import json
import math
from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/social_distancing', methods=['POST'])
def evaluate_socialdistance():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    
    def choose(n, r):
        return int(math.factorial(n) / (math.factorial(r) * math.factorial(n-r)))

    output = {}
    output['answers'] = {}
    tests = data["tests"]
    for key in tests.keys():
        seats = tests[key]["seats"]
        people = tests[key]["people"]
        spaces = tests[key]["spaces"] 
        output['answers'][key] = choose(seats - (people-1)*spaces, people)
    
    logging.info("My result :{}".format(output))
    return json.dumps(output)



