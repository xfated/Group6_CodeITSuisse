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
            future_pro = round_ratio/(j["IndexFuturePrice"] * j["Notional"])
            name = j['Name']
            vol = j['FuturePrcVol']                              

            if not any(lowest):
                lowest['Name'], lowest['Vol'], lowest['Ratio'], lowest['Fut'] = name, vol, ratio, future_pro
            else:
                # this future has lower vol and ratio
                if lowest['Vol'] > vol and lowest['Ratio'] > ratio:     
                    lowest['Name'], lowest['Vol'], lowest['Ratio'], lowest['Fut'] = name, vol, ratio, future_pro
                # this future has lower vol or ratio
                elif lowest['Vol'] > vol and lowest['Ratio'] < ratio:
                    #compare lowest number of futures proportion 
                    if lowest['Fut'] > future_pro:
                        lowest['Name'], lowest['Vol'], lowest['Ratio'], lowest['Fut'] = name, vol, ratio, future_pro
                elif lowest['Vol'] < vol and lowest['Ratio'] > ratio:
                    if lowest['Fut'] > future_pro:
                        lowest['Name'], lowest['Vol'], lowest['Ratio'], lowest['Fut'] = name, vol, ratio, future_pro
        
        best_index['HedgePositionName'] = lowest['Name']
        best_index['OptimalHedgeRatio'] = lowest['Ratio']
        best_index['NumFuturesContract'] = round(lowest['Fut'] * value)
        output.append(best_index)

    # publish result
    logging.info("My result :{}".format(output))
    result = { "outputs" : output}
    return json.dumps(result)
