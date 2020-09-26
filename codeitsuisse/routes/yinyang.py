import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/yin-yang', methods=['POST'])
def evaluate_yinyang():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    
    no_Elements = data['number_of_elements']
    no_Operations = data['number_of_operations']
    elements = data['elements']

    # yin_count = 0
    # yang_count = 0
    # for char in elements:
    #     if char == "y":
    #         yin_count += 1
    #     else:
    #         yang_count += 1
    
    def get_yang_probability(seq, picks_left, sum, first = False):
        possible_yang = 0
        element_count = len(seq)
        p_Y = 0
        yang_indexes = set()
        # element_count = no_Elements - pick_no + 1
        for p_i in range(0, element_count): # p_i = possible index. == number of elements left
            print(seq, p_i, seq[p_i], seq[element_count - p_i -1])
            if seq[p_i] == "Y" or seq[element_count - p_i - 1] == "Y":
                possible_yang += 1
            if seq[p_i] == "Y":
                yang_indexes.add(p_i)
            if seq[element_count - p_i - 1] == "Y":
                yang_indexes.add(element_count - p_i - 1)
        p_Y = possible_yang / len(seq)
        
        if picks_left == 1:
            print('no picks left', p_Y)
            return p_Y
        
        new_sum = sum
        split = 1/len(yang_indexes)
        for index in yang_indexes:
            val = split * p_Y * get_yang_probability(seq[:index]+seq[index+1:], picks_left - 1, sum)
            print('val', val)
            new_sum += val

        if first:
            new_sum += p_Y
            
        return new_sum

    result = get_yang_probability(elements,no_Operations,0, True)
    
    logging.info("My result :{}".format(result))
    return json.dumps(result)



