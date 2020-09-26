import logging
import json
import math

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/optimizedportfolio', methods=['POST'])

def evaluate_portfolio():                              ## Main Function
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    def normal_round(n, decimals):
        expoN = n * 10 ** decimals
        if abs(expoN) - abs(math.floor(expoN)) < 0.5:
            return math.floor(expoN) / 10 ** decimals
        return math.ceil(expoN) / 10 ** decimals

    def normal(n):
        return math.ceil(n)


    #get data
    inputs = data['inputs']

    # Number of futures contract should use ROUND to the nearest whole number.
    # Optimal Hedge ratio should use ROUND to 3 decimal places.
    
    output = []
    for i in inputs:                                    #loop thru the dictionary
        port = i['Portfolio']
        index = i['IndexFutures']
        
        #Consider only between volatility of futures and ratio first 
        #Portfolio details
        value = port['Value']
        port_vol = port['SpotPrcVol']
        best_index = {}

        lowest = {}
        for j in index:                         #loop thru the indexes 
            ratio =  j["CoRelationCoefficient"] * (port_vol / j["FuturePrcVol"])
            round_ratio = normal_round(ratio,3)
            future_pro = round_ratio*value/(j["IndexFuturePrice"] * j["Notional"])
            future_round = normal(future_pro)
            name = j['Name']
            vol = j['FuturePrcVol']                              

            if not any(lowest):
                lowest['Name'], lowest['Vol'], lowest['Ratio'], lowest['Fut'], lowest['ratio'], lowest['fut'] = name, vol, round_ratio, future_round, ratio, future_pro
            else:
                # this future has lower vol and ratio
                if lowest['Vol'] > vol and lowest['ratio'] > ratio:     
                    lowest['Name'], lowest['Vol'], lowest['Ratio'], lowest['Fut'], lowest['ratio'], lowest['future'] = name, vol, round_ratio, future_round, ratio, future_pro
                # this future has lower vol or ratio
                elif lowest['Vol'] > vol and lowest['ratio'] < ratio :
                    if lowest['fut'] > future_pro:
                        lowest['Name'], lowest['Vol'], lowest['Ratio'], lowest['Fut'], lowest['ratio'], lowest['future'] = name, vol, round_ratio, future_round, ratio, future_pro
                elif lowest['Vol'] < vol and lowest['ratio'] > ratio:
                    if lowest['fut'] > future_pro:
                        lowest['Name'], lowest['Vol'], lowest['Ratio'], lowest['Fut'], lowest['ratio'], lowest['future'] = name, vol, round_ratio, future_round, ratio, future_pro
                # Same metrics 
                # elif lowest['Vol'] == vol or lowest['Ratio'] == round_ratio:
                #     if lowest['Fut'] > future_round:
                #         lowest['Name'], lowest['Vol'], lowest['Ratio'], lowest['Fut'], lowest['ratio'], lowest['future'] = name, vol, round_ratio, future_round, ratio, future_pro


        best_index['HedgePositionName'] = lowest['Name']                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
        best_index['OptimalHedgeRatio'] = lowest['Ratio']
        best_index['NumFuturesContract'] = lowest['Fut'] 
        output.append(best_index)

    # publish result
    logging.info("outputs:{}".format(output))
    result = { "outputs": output}
    return json.dumps(result) 