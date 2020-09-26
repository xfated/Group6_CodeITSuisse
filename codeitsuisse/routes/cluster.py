import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/cluster', methods=['POST'])
def evaluate_cluster():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    
    area = data
    
    rows = len(area)
    cols = len(area[0])

    ufds = UnionFind(rows*cols + 1)
    for row in range(rows):
        for col in range(cols):
            if area[row][col] == "*":
                continue
            else:
                center_pos = row*cols + (col + 1)
                infectious = False
                if area[row][col] == "1":
                    infectious = True
                if (row != rows-1): 
                    # bottom
                    if area[row+1][col] != "*":
                        if area[row+1][col] == "1":
                            infectious = True
                        other_pos = (row+1)*cols + col+1
                        ufds.union(center_pos, other_pos, infectious)
                if (col != cols-1):
                    # right
                    if area[row][col+1] != "*":
                        if area[row][col+1] == "1":
                            infectious = True
                        other_pos = (row)*cols + col+1+1
                        ufds.union(center_pos, other_pos, infectious)
                if (col != cols-1) and (row != rows-1):
                    # diagonal right
                    if area[row+1][col+1] != "*":
                        if area[row+1][col+1] == "1":
                            infectious = True
                        other_pos = (row+1)*cols + col+1+1
                        ufds.union(center_pos, other_pos, infectious)
                if (col != 0) and (row != rows-1):
                    # diagonal left
                    if area[row+1][col-1] != "*":
                        if area[row+1][col-1] == "1":
                            infectious = True
                        other_pos = (row+1)*cols + col-1+1
                        ufds.union(center_pos, other_pos, infectious)


    clusters = 0
    for key in ufds.clusters.keys():
        if ufds.clusters[key] == True:
            clusters += 1

    answer = {}
    answer["answer"] = clusters
    logging.info("My result :{}".format(answer))
    return json.dumps(answer)


class UnionFind:
    def __init__(self, N):
        self.rank = [0 for _ in range(N)]
        self.parent = [i for i in range(N)]
        self.groups = N
        self.clusters = {}
        
    def find(self, i):
        if self.parent[i] == i: return i
        self.parent[i] = self.find(self.parent[i]) #path compression
        return self.parent[i]
    
    def union(self, i, j, infectious): 
        x, y = self.find(i), self.find(j)
        if x != y:
            if self.rank[x] > self.rank[y]: 
                if y in self.clusters.keys():
                    self.clusters.pop(y)
                if x in self.clusters.keys():
                    if self.clusters[x] != True:
                        if infectious:
                            self.clusters[x] = True
                else:
                    self.clusters[x] = infectious
                self.parent[y] = x
                
            else:
                self.parent[x] = y

                if x in self.clusters.keys():
                    self.clusters.pop(x)
                if y in self.clusters.keys():
                    if self.clusters[y] != True:
                        if infectious:
                            self.clusters[y] = True
                else:
                    self.clusters[y] = infectious

                if self.rank[x] == self.rank[y]: self.rank[y] += 1
            self.groups -= 1

