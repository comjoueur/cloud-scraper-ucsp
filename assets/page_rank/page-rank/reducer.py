#! /usr/bin/python3

from sys import stdin

nodes = {}
d = 0.15  # damping_factor
n = 224  # total_nodes

for line in stdin:
    tag, node_id, pagerank = line.strip().split(" ")
    if not nodes.get(node_id, False):
        nodes[node_id] = [0.0, 0.0]  # [previous_pagerank,new_pagerank]
    if tag == "node":
        nodes[node_id][0] = float(pagerank)
    else:
        nodes[node_id][1] += float(pagerank)

for node in nodes:
    random_walk = d / n
    update_pagerank = random_walk + (1 - d) + nodes[node][1]
    print("{} {}".format(node, update_pagerank))
