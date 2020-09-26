import logging
import json
import Levenshtein
import operator

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/inventory-management', methods=['POST'])
def evaluate_inventory():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    resLst = []
    for d in data:
        target = d['searchItemName'].lower()
        items = d['items']
        items = [i.lower() for i in items]

        itemLst = []
        for i in items:
            res = target
            target_copy = target
            dist = Levenshtein.distance(target, i)

            counter = 0
            for edit in Levenshtein.editops(target, i):
                if edit[0] == 'delete':
                    res = res[:edit[1]+counter] + '-' + res[edit[1]+counter:]
                    counter += 1
                elif edit[0] == 'insert':
                    res = res[:edit[1]+counter] + f'+{i[edit[2]]}' + res[edit[1]+counter:]
                    counter += 2 
                elif edit[0] == 'replace':
                    res = res[:edit[1]+counter] + f'{i[edit[2]]}' + res[edit[1]+counter+1:]
                    counter += 1
            itemLst.append((res, dist))
        
        itemLst = sorted(itemLst, key=operator.itemgetter(1, 0))
        itemLst = [x[0] for x in itemLst][:10]
        result = {'searchItemName': d['searchItemName'], 'searchResult': itemLst}
        resLst.append(result)

    logging.info("My result :{}".format(resLst))
    return json.dumps(resLst)



