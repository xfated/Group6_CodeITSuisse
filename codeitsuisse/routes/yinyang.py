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

    y_count = 0
    Y_count = 0
    for char in elements:
        if char == 'y':
            y_count += 1
        else:
            Y_count += 1
    

    tried_dict = {}
    def get_yang_probability(seq, picks_left, sum, yinCount, yangCount, yangChosen, tried, first = False):
        if (yinCount == yangCount):
            if picks_left % 2 == 0:
                return picks_left / 2
            else:
                return picks_left / 2 + 1 
        
        possible_yang = 0
        element_count = len(seq)
        p_Y = 0
        yang_indexes = set()
        desired_char = ''
        
        if yinCount < yangCount:
            desired_char = 'Y'
            yangChosen += 1
            yangCount -= 1 
        else:
            desired_char = 'y'
            yinCount -= 1 
        # element_count = no_Elements - pick_no + 1
        if (seq, desired_char) in tried.keys():
            p_Y, yang_indexes = tried[(seq, desired_char)]
        else:
            for p_i in range(0, int(element_count+1/2)): # p_i = possible index. == number of elements left
                if seq[p_i] == desired_char or seq[element_count - p_i - 1] == desired_char:
                    possible_yang += 1
                if seq[p_i] == desired_char:
                    yang_indexes.add(p_i)
                if seq[element_count - p_i - 1] == desired_char:
                    yang_indexes.add(element_count - p_i - 1)
            p_Y = possible_yang / len(seq)
            tried[(seq, desired_char)] = (p_Y, yang_indexes)
            tried[(seq[::-1], desired_char)] = (p_Y, yang_indexes)
        
        picks_left -= 1
        if picks_left == 1:
            # print(seq, yang_indexes, desired_char)
            return p_Y * yangChosen  

            
        new_sum = sum
        split = 1/len(yang_indexes)
        for index in yang_indexes:
            new_seq = seq[:index]+seq[index+1:]
            # val = 0
            # if (split, p_Y, new_seq, picks_left, sum, yinCount, yangCount) in tried.keys():
            #     val = tried[(split, p_Y, new_seq, picks_left, sum, yinCount, yangCount)]
            # else:
            val = yangChosen * split * p_Y * get_yang_probability(new_seq, picks_left, sum, yinCount, yangCount, yangChosen, tried)
                # tried[frozenset((split, p_Y, new_seq, picks_left, sum, yinCount, yangCount))] = val
            new_sum += val

        if first:
            new_sum += p_Y
        return new_sum

    result = get_yang_probability(elements,no_Operations,0, y_count, Y_count, 0, tried_dict, True)
    
    logging.info("My result :{}".format(result))
    return json.dumps(result)



