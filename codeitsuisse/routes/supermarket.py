import logging
import json
from collections import deque

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/supermarket', methods=['POST'])
def evaluate_supermarket():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    result = {'answers': {}}
    for d in data['tests']:
        maze = data['tests'][d]['maze']
        start = data['tests'][d]['start']
        end = data['tests'][d]['end']

        ROW = len(maze)
        COL = len(maze[0])

        class Point: 
            def __init__(self, x, y): 
                self.x = x 
                self.y = y 
        
        class queueNode: 
            def __init__(self, pt, dist): 
                self.pt = pt  
                self.dist = dist 
        
        def isValid(row, col): 
            return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL) 
        
        rowNum = [-1, 0, 0, 1] 
        colNum = [0, -1, 1, 0]

        def BFS(mat, src, dest): 
        
            if mat[src.x][src.y]!=0 or mat[dest.x][dest.y]!=0:
                return -1
            
            visited = [[False for i in range(COL)] for j in range(ROW)] 
            visited[src.x][src.y] = True
            
            q = deque() 
            s = queueNode(src,0) 
            q.append(s)
            
            while q: 
        
                curr = q.popleft()
                
                pt = curr.pt 
                if pt.x == dest.x and pt.y == dest.y: 
                    return curr.dist 
                
                for i in range(4): 
                    row = pt.x + rowNum[i] 
                    col = pt.y + colNum[i] 
                    
                    if (isValid(row,col) and mat[row][col] == 0 and not visited[row][col]): 
                        visited[row][col] = True
                        Adjcell = queueNode(Point(row,col),curr.dist+1) 
                        q.append(Adjcell) 
            
            return -1
        
        source = Point(start[1], start[0]) 
        dest = Point(end[1], end[0]) 
        
        dist = BFS(maze, source, dest) 
        
        if dist != -1: 
            res = (dist+1) 
        else: 
            res = -1

        result['answers'][d] = res

    logging.info("My result :{}".format(result))
    return json.dumps(result)



