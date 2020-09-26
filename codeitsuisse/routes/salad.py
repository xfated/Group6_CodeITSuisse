import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/salad-spree', methods=['POST'])
def evaluate_saladspree():                              ## Main Function
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    #get data
    n = data['number_of_salads']
    streets = data["salad_prices_street_map"]
    final_cost = 10000000000

    def count_X(street):
        count = street.count('X')
        return count

    def consec_num(n,street):
        final_num = 0
        temp = 0
        list_of_stores = []
        store = []
        for i in street:
            if i != 'X':
                temp += 1
                store.append(i)
            else:
                if temp > final_num:
                    final_num = temp
                    temp = 0
                    list_of_stores.append(store)
                    store = []
        return final_num, list_of_stores

    def get_cheapest_consec(n,street):
        min_sum = 1000000000
        for i in street:
            temp = 0
            if len(i) == n:                         #only this consec stores
                for j in i:
                    temp += int(j)
                min_sum = temp
                return min_sum
            elif len(i) > n:                        #stores more than n 
                for x in range(len(i)):
                    if n + x < len(i):
                        for y in i[x:n+x]:
                            temp += int(y)
                            if temp < min_sum:
                                min_sum = temp
                return min_sum

    cheapest = 10000000000000000
    # for i in streets:
        # consec, stores = consec_num(n,i)
        # if len(i) - count_X(i) < n:                 #if street does not have enough salads
        #     temp = 0
        # elif consec < n:                            #check if have enough consecutive stores
        #     temp = 0                             
        # else:
        #     cost = get_cheapest_consec(n,stores)
        #     if cost < final_cost:
        #         final_cost = cost

    for street in streets:
        cur_cost = 0
        count = 0
        for j in range(len(street)):
            if street[j] != 'X':
                cur_cost += int(street[j])
                count += 1
                if count == n:
                    if cur_cost < cheapest:
                        cheapest = cur_cost
                elif count > n:
                    cur_cost -= int(street[j-n])
                    if cur_cost < cheapest:
                        cheapest = cur_cost
            else:
                print(cur_cost)
                if cur_cost < cheapest and count == n:
                    cheapest = cur_cost
                cur_cost = 0
                count = 0
        
                
    if cheapest == 10000000000000000:
        final_cost = 0
    else:
        final_cost = cheapest
    # publish result
    logging.info("result: {}".format(final_cost))
    result = {"result": final_cost}
    return json.dumps(result)



            


