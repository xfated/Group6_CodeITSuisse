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
    def get_yang_probability(seq, picks_left, sum, yinCount, yangCount, tried, first = False, prevProb = 1):
        
        possible_yang = 0
        element_count = len(seq)
        p_Y = 0
        yang_indexes = set()
        desired_char = 'Y'
        
        # if yinCount < yangCount:
        #     desired_char = 'Y'
        #     yangCount -= 1 
        # else:
        #     desired_char = 'y'
        #     yinCount -= 1

        # element_count = no_Elements - pick_no + 1
        if (seq, desired_char) in tried.keys():
            p_Y, yang_indexes = tried[(seq, desired_char)]
        else:
            for p_i in range(0, int(element_count)): # p_i = possible index. == number of elements left
                # print(seq, p_i, seq[p_i], seq[element_count - p_i - 1])
                if seq[p_i] == desired_char or seq[element_count - p_i - 1] == desired_char:
                    possible_yang += 1
                if seq[p_i] == desired_char:
                    yang_indexes.add(p_i)
                if seq[element_count - p_i - 1] == desired_char:
                    yang_indexes.add(element_count - p_i - 1)
            p_Y = possible_yang / len(seq)
            # print(seq, p_Y)
            tried[(seq, desired_char)] = (p_Y, yang_indexes)
            tried[(seq[::-1], desired_char)] = (p_Y, yang_indexes)
        

        if picks_left == 1 or prevProb < 0.00000000001 or len(yang_indexes) == 0:
            # print("final", seq, p_Y)
            if desired_char == "Y":
                return prevProb * p_Y 
            else:
                return 0
        picks_left -= 1


        # print(prevProb, p_Y)
        new_sum = sum
    
        if desired_char == "Y":
            new_sum  += prevProb * p_Y
            
        # if first:
        #     if desired_char == "Y":
        #         new_sum += p_Y
        
        sums = 0
        total = 0
        new_sets = {}
        for index in yang_indexes:
            new_seq = seq[:index]+seq[index+1:]
            new_sets[new_seq] = new_sets.get(new_seq,0) + 1
            total += 1
            # val = 0
            # if (split, p_Y, new_seq, picks_left, sum, yinCount, yangCount) in tried.keys():
            #     val = tried[(split, p_Y, new_seq, picks_left, sum, yinCount, yangCount)]
            # else:
                # tried[frozenset((split, p_Y, new_seq, picks_left, sum, yinCount, yangCount))] = val
            # new_sum += val
        for new_seq in new_sets.keys():
            split = new_sets[new_seq]/total
            sums += get_yang_probability(new_seq, picks_left, sum, yinCount, yangCount, tried, prevProb = p_Y*split)
            
        new_sum += sums

        return new_sum

    result = get_yang_probability(elements,no_Operations,0, y_count, Y_count, tried_dict, True)
    result = float("{:.10f}".format(result))
    logging.info("My result :{}".format(result))
    return json.dumps(result)



