import logging
import json
from shapely.geometry import Polygon, LineString
from shapely.geometry.multilinestring import MultiLineString

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/revisitgeometry', methods=['POST'])
def evaluate_revisitgeometry():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    shapeCoordinates = data['shapeCoordinates']
    lineCoordinates = data['lineCoordinates']

    shape = []
    for s in shapeCoordinates:
        x = s['x']
        y = s['y']
        shape.append((x,y))

    line = []
    for l in lineCoordinates:
        x = l['x']
        y = l['y']
        line.append((x,y))

    # print(shape, line)
    grad = (line[1][1] - line[0][1]) / (line[1][0] - line[0][0])
    new_y = ((999 - line[1][0]) * grad) + line[1][1]
    new_coor = (999, new_y)
    line.append(new_coor)
    new_y2 = ((-999 - line[1][0]) * grad) + line[1][1]
    new_coor2 = (-999, new_y2)
    line.append(new_coor2)

    if len(shape) == 2:
        shapely_poly = LineString(shape)
    else:
        shapely_poly = Polygon(shape)
    shapely_line = LineString(line)

    intersection_line = []
    if type(shapely_poly.intersection(shapely_line)) is MultiLineString:
        for inte in shapely_poly.intersection(shapely_line):
            intersection_line += list(inte.coords)
    else:
        intersection_line = list(shapely_poly.intersection(shapely_line).coords)
    intersection_line = list(set(intersection_line))

    result = []
    for i in intersection_line:
        x = round(i[0], 2)
        y = round(i[1], 2)
        
        if x % 1 == 0.0:
        
            x = round(x)
        if x % 1 == 0.0:
            y = round(y)
        result.append({'x': x, 'y': y})
    
    logging.info("My result :{}".format(result))
    return json.dumps(result)



