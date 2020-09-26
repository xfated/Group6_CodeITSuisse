import logging
import json
import math

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/driverless-car', methods=['POST'])
def evaluate_driverless():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    
    gameId = data['gameId']
    roads = data['roads']


    logging.info("My result :{}".format(result))
    return json.dumps(result)


class Road:
    def __init__(self, _name, _type, _towards, _from, _maxSpeed, _zones):
        self.name = _name
        self.type = _type
        self.start = (_from["x"], _from["y"])
        self.end = (_towards["x"], _towards["y"])
        self.maxSpd = _maxSpeed
        self.zones = []
        zone_dict = {}
        for zone in _zones:
            initPos = (zone['from']['x'], zone['from']['y'])
            finalPos =  (zone['to']['x'], zone['to']['y'])
            speed = zone['maxSpeed']
            if self.type == "street": # x value varies
                zone_dict[initPos[0]] = (initPos, finalPos, maxSpeed)
            else: # y value varies
                zone_dict[initPos[1]] = (initPos, finalPos, maxSpeed)

            # sort by key, so the first zone will be first in list
            for key in list(zone_dict.keys()).sort():
                self.zones.append(zone_dict[key])
                        
    # given init spd, final spd and acc, return dist
    def calcDist(self, initSpd, finalSpd, Acc):
        time = (finalSpd - initSpd) / Acc
        return initSpd*time + 1/2 * Acc * time * time #s = ut + 1/2 at^2

    # given init spd, acceleration and distance, return final spd
    def calcSpd(self, initSpd, Acc, Dist):
        return math.sqrt(initSpd * initSpd + 2 * Acc * Dist)

    def getInstructionsStart2End(self, initSpd, finalSpd, topSpd, Acc, Decc) #instructions to go from start to end
        instructions = []
        firstZone = self.zones[0]
        next_spd = 0
        if len(self.zones) > 0:
            for i in range(len(self.zones)):
                zone_initPos, zone_finalPos, zone_maxSpd = self.zones[i]
                if i == 0: # first zone
                    # get instructions to first zone
                    instr = {}
                    dist = abs(self.start[0] - zone_initPos[0] + self.start[1] - zone_initPos[1])
                    dist_to_acc = self.calcDist(initSpd, zone_maxSpd, Acc)
                    if dist_to_acc > dist: #takes too long to accelerate:
                        nextSpd = calcSpd(initSpd, Acc, dist)
                        
                elif i == len(self.zones) - 1: #last zone

            
        for zone in self.zones:
            dist = self.calcDist(initSpd, finalSpd, maxSpd)
