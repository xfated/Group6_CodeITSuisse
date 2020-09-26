import logging
import json
import operator

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/olympiad-of-babylon', methods=['POST'])
def evaluate_babylon():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    
    # get data
    numBooks = data['numberOfBooks']
    numDays = data['numberOfDays']
    books = data['books']
    days = data['days']

    all_indexes = set([i for i in range(numBooks)])

    day_choices = {}
    for i in range(numDays):
        possibleCombi = []
        queue = [([index], books[index]) for index in all_indexes if books[index] < days[i]]
        tried_indexes = set([frozenset(indexes) for indexes, duration in queue])
        while len(queue) > 0:
            indexes, duration = queue.pop(0)
            for j in range(numBooks):
                if j not in indexes:
                    newset = frozenset(indexes + [j])
                    if newset not in tried_indexes:
                        tried_indexes.add(newset)
                        if duration + books[j] < days[i]:
                            queue.append((indexes + [j] , duration + books[j]))
                        else:
                            possibleCombi.append(indexes)
        day_choices[i] = possibleCombi
        # val = max(possibleCombi.values())
        # result = [k for k,v in possibleCombi.items() if v == val]
        # day_choice = result[0]
        # for i in day_choice:
        #     all_indexes.discard(i)
        # optim_no += len(day_choice)
    queue = day_choices[0]

    optim_no = 0
    for i in range(1, numDays):
        for j in range(len(queue)):
            prev_option = queue.pop(0)
            for option in day_choices[i]:
                if set(option) & set(prev_option): #there are common elements
                    continue
                else:
                    sum_books = len(option) + len(prev_option)
                    if sum_books > optim_no:
                        optim_no = sum_books 
                    queue.append(prev_option+option)

    # publish result
    logging.info("My result :{}".format(optim_no))
    result = { "optimalNumberOfBooks" : optim_no}
    return json.dumps(result)



