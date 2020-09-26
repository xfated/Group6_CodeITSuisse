import logging
import json
import math
from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/clean_floor', methods=['POST'])
def evaluate_cleanfloor():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    tests = data['tests']
    output = {}
    output['answers'] = {}
    for key in tests.keys():
        answer = 0
        floor = tests[key]['floor']
        for i in range(len(floor) - 1):
            answer += 2*floor[i]

            if floor[i] > floor[i+1]:
                diff = floor[i] - floor[i+1]
                if diff % 2 == 0:
                    floor[i+1] = 0
                else:
                    floor[i+1] = 1
            else:
                floor[i+1] = floor[i+1] - floor[i]
            
            if (i != len(floor)-2):
                if floor[i+1] > 0:
                    floor[i+1] -= 1
                else:
                    floor[i+1] += 1
                answer += 1 

        if (floor[len(floor)-1] != 0):
            floor[len(floor)-1] -= 1
            answer += 1

            if floor[len(floor)-1] % 2 != 0: #last is odd
                answer += 1

            answer += 2 * floor[len(floor)-1]

        output['answers'][key] = answer
        
    logging.info("My result :{}".format(output))
    return json.dumps(output)

#14998


