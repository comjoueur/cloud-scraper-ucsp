#!/usr/bin/env python3
from sys import stdin


for line in stdin:
    node_id, adj_nodes, pagerank = line.strip().split(" ")

    adj_nodes = adj_nodes.split(",")

    print("node {} {}".format(node_id, pagerank))

    out_pgrank = float(pagerank) / len(adj_nodes)

    for node in adj_nodes:
        print("pagerank {} {}".format(node, out_pgrank))
