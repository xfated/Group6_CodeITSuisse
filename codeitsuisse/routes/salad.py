# import logging
# import json

# from flask import request, jsonify;

# from codeitsuisse import app;

# logger = logging.getLogger(__name__)

# @app.route('/salad-spree', methods=['POST'])

# You should be expecting the number of required salads to be smaller or equal to the number of shops per street. Both of these numbers should not exceed 100. 
# will only buy salad from stores that are next to each other
import re

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
            

def salad_cost(n,streets):
    final_cost = 10000000000
    for i in streets:
        consec, stores = consec_num(n,i)
        if len(i) - count_X(i) < n:                 #if street does not have enough salads
            temp = 0
        elif consec < n:                     #check if have enough consecutive stores
            temp = 0                             
        else:
            cost = get_cheapest_consec(n,stores)
            if cost < final_cost:
                final_cost = cost
                
    if final_cost == 10000000000:
        final_cost = temp
    return (f'result : {final_cost}')

            

            

