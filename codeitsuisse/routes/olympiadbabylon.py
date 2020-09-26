import logging
import json

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

    books.sort()
    days.sort()

    print(books)
    print(days)
    
    optim_no = 0
    used_indexes = set()

    j = 0
    for time in days:
        current_sum = 0
        for i in range(j,numBooks):
            print(i)
            if current_sum + books[i] < time:
                current_sum += books[i]
                used_indexes.add(i)
                print(time, books[i])
                j = i + i
    optim_no = len(used_indexes)

    # publish result
    logging.info("My result :{}".format(optim_no))
    result = { "optimalNumberOfBooks" : optim_no}
    return json.dumps(result)



