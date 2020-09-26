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

    # get books in dict
    book_dict = {}
    for i in range(len(books)):
        book_dict[i] = books[i]
     

    result = 0

    # publish result
    logging.info("My result :{}".format(result))
    return json.dumps(result)



