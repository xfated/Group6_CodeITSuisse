import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/optimizedportfolio', methods=['POST'])

def evaluate_portfolio():                              ## Main Function
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    #get data
    inputs = data['inputs']

    # Number of futures contract should use ROUND to the nearest whole number.
    # Optimal Hedge ratio should use ROUND to 3 decimal places.
    
    output = []
    for i in inputs:                                    #loop thru the dictionary
        port = i['Portfolio']
        index = i['IndexFutures']
        
        #Consider only between volatility of futures and ratio for conclusion
        #Port details
        value = port['Value']
        port_vol = port['SpotPrcVol']
        best_index = {}

        lowest = {}
        for j in index:                         #loop thru the indexes 
            ratio =  j["CoRelationCoefficient"] * (port_vol / j["FuturePrcVol"])
            round_ratio = round(ratio,3)
            future_pro = round_ratio*value/(j["IndexFuturePrice"] * j["Notional"])
            future_round = round(future_pro)
            name = j['Name']
            vol = j['FuturePrcVol']                              

            if not any(lowest):
                lowest['Name'], lowest['Vol'], lowest['Ratio'], lowest['Fut'] = name, vol, round_ratio, future_round
            else:
                # this future has lower vol and ratio
                if lowest['Vol'] > vol and lowest['Ratio'] > ratio:     
                    lowest['Name'], lowest['Vol'], lowest['Ratio'], lowest['Fut'] = name, vol, round_ratio, future_round
                # this future has either lower vol or ratio
                elif (lowest['Vol'] > vol and lowest['Ratio'] < ratio) or (lowest['Vol'] < vol and lowest['Ratio'] > ratio):
                    #compare lowest number of futures proportion 
                    if lowest['Fut'] > future_pro:
                        lowest['Name'], lowest['Vol'], lowest['Ratio'], lowest['Fut'] = name, vol, round_ratio, future_round
                # elif lowest['Vol'] < vol and lowest['Ratio'] > ratio:
                #     if lowest['Fut'] > future_pro:
                #         lowest['Name'], lowest['Vol'], lowest['Ratio'], lowest['Fut'] = name, vol, round_ratio, future_round
        
        best_index['HedgePositionName'] = lowest['Name']
        best_index['OptimalHedgeRatio'] = lowest['Ratio']
        best_index['NumFuturesContract'] = lowest['Fut'] 
        output.append(best_index)

    # publish result
    logging.info("My result :{}".format(output))
    result = { "outputs": output}
    return json.dumps(result) 