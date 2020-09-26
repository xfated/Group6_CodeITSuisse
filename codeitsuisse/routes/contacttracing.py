import logging
import json
from collections import Counter

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/contact_trace', methods=['POST'])
def evaluate_contacttracing():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    def alterations(genome1, genome2): # count number of alterations btw genome1 and genome2, but if instruction is changed totally, return 999
        # genome1 = genome1.split('-')
        # genome2 = genome2.split('-')
        res = 0
        for i in range(len(genome1)):
            if genome1[i] != genome2[i]:
                res += 1
        # for i in range(len(genome1)):
        #     for j in range(len(genome1[0])):
        #         if genome1[i][j] != genome2[i][j]:
        #             res += 1   
        #     shared = sum((Counter(genome1[i]) & Counter(genome2[i])).values())
        #     if genome1[i] != genome2[i] and shared >= 1:
        #         res += 1
        #     elif shared == 0:
        #         res += 999
        #         break
        return res
    
    def nonsilent(genome1, genome2):
        genome1 = genome1.split('-')
        genome2 = genome2.split('-')
        res = 0
        for i in range(len(genome1)):
            if genome1[i][0] != genome2[i][0]:
                return True
        return False

    infected_name = data['infected']['name']
    infected_genome = data['infected']['genome']

    origin_name = data['origin']['name']
    origin_genome = data['origin']['genome']

    cluster = data['cluster']
    cluster_name = []
    cluster_genome = []
    for i in cluster:
        cluster_name.append(i['name'])
        cluster_genome.append(i['genome'])

    result = []
    min_alterations = 20

    if infected_genome == origin_genome:
        trace = f'{infected_name} -> {origin_name}'
        result.append((trace, 0))

        for i in range(len(cluster_name)):
            if cluster_genome[i] == infected_genome:
                trace = f'{infected_name} -> {cluster_name[i]}'
                result.append((trace, 0))   
    else:
        # handle clusters
        for i in range(len(cluster_name)):
            if alterations(infected_genome, cluster_genome[i]) <= min_alterations:
                min_alterations = alterations(infected_genome, cluster_genome[i])
                if nonsilent(infected_genome, cluster_genome[i]):
                    trace = f'{infected_name}* -> {cluster_name[i]}'
                else:
                    trace = f'{infected_name} -> {cluster_name[i]}'
            
            if alterations(cluster_genome[i], origin_genome) <= min_alterations:
                if nonsilent(cluster_genome[i], origin_genome):
                    trace += f'* -> {origin_name}'
                else:
                    trace += f' -> {origin_name}'
            result.append((trace, min_alterations))
            
        if alterations(infected_genome, origin_genome) <= min_alterations: 
            min_alterations = alterations(infected_genome, origin_genome)
            if nonsilent(infected_genome, origin_genome):
                trace = f'{infected_name}* -> {origin_name}'
            else:
                trace = f'{infected_name} -> {origin_name}'
            result.append((trace, 0))
    
    new_result = []
    for trace, alterations in result:
        if alterations <= min_alterations:
            new_result.append(trace)
    logging.info("My result :{}".format(new_result))
    return json.dumps(new_result)



