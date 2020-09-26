import logging
import json

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
        floor = [0] + tests[key]['floor'] + [0]
        cur_sum = sum(floor)
        cur_index = 1
        while(cur_sum > 0):
            if floor[cur_index-1] > floor[cur_index+1]:
                cur_index -= 1
            elif floor[cur_index-1] == floor[cur_index+1]:
                if sum(floor[:cur_index])>sum(floor[cur_index:]):
                    cur_index -=1
                else:
                    cur_index +=1
            else:    
                cur_index += 1
            if floor[cur_index] > 0:
                floor[cur_index] -= 1
                cur_sum -=1
            else:
                floor[cur_index]  += 1
                cur_sum += 1
            answer += 1
        output['answers'][key] = answer
        
    logging.info("My result :{}".format(output))
    return json.dumps(output)



