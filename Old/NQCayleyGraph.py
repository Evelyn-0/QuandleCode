# This script computes the Cayley graph for an N-quandle (if finite)
# This version replicates the Mathematica program
# It stores the directed edges of the graph as a list of triples (start, end, label)

import time
import math
import os
from tabulate import tabulate
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt 
from pyvis.network import Network

ALPHABET = list('abcdefghijklmnopqrstuvwxyz')

# Collapse the set of edges
def collapse(Edges, Vertices):
    done = False
    while not done: # repeat loop as long as a change was made
        done = True
        replace = {} # dictionary of vertex replacements, old:new
        for i in range(len(Edges)):
            for j in range(i+1,len(Edges)):
                if Edges[i][2] == Edges[j][2]: # if two edges have the same label
                    # if they start at the same vertex, merge the endpoints
                    if Edges[i][0] == Edges[j][0]:
                        if Edges[i][1] != Edges[j][1]:
                            # replace larger vertex with smaller
                            replace[max(Edges[i][1],Edges[j][1])] = min(Edges[i][1],Edges[j][1])
                            done = False
                    # if they end at the same vertex, merge the starting points
                    elif Edges[i][1] == Edges[j][1]:
                        replace[max(Edges[i][0],Edges[j][0])] = min(Edges[i][0],Edges[j][0])
                        done = False
        if not done:
            # Go through the edges and replace vertices
            # Keep replacing, in case there is a chain (replace a with b, and b with c)
            for e in range(len(Edges)):
                while Edges[e][0] in replace:
                    Edges[e] = (replace[Edges[e][0]], Edges[e][1], Edges[e][2])
                while Edges[e][1] in replace:
                    Edges[e] = (Edges[e][0], replace[Edges[e][1]], Edges[e][2])
        Edges = list(set(Edges)) # remove duplicates
        for v in replace:
            Vertices.remove(v) # remove vertices that were collapsed
            
    return Vertices, Edges

# Add secondary relations at a vertex, then collapse redundant edges.
def add_relations(vertex, relations, Vertices, Edges):
    for rel in relations:
        v1 = vertex
        v2 = max(Vertices) + 1 # new vertex
        for w in rel[:len(rel)-1]:
            if w > 0:  # add all edges with positive labels
                Edges.append((v1, v2, w))
            else:
                Edges.append((v2, v1, -w))
            Vertices.add(v2) # add new vertex to list of vertices
            v1 = v2
            v2 = v2 + 1
        # final edge returns to original vertex
        if rel[len(rel)-1] > 0:  # add all edges with positive labels
            Edges.append((v1, vertex, rel[len(rel)-1]))
        else:
            Edges.append((vertex, v1, -rel[len(rel)-1]))
        Vertices, Edges = collapse(Edges, Vertices)
        
    return Vertices, Edges

# gen is a number of generators
# init is the list of initial relations a^{g_1g_2...g_k} = b, in the form [a, g_1, ..., g_k, b]
# sec is the list of secondary relations x^{g_1...g_k} = x, in the form [g_1, ..., g_k]
# Each generator is represented by an integer from 1 to generators
def q_graph(gen, init):
    Vertices = set({}) # set of vertices.  Vertices are represented as positive integers.
    Edges = [] # list of edges. Each edge is a tuple (start, end, label)

    sec = []

    for i in range(gen):
        sec.append([i+1, i+1])

    for i in init[0:-1]:
        start = i[0]
        end = i[-1]
        exp = i[1:-1]
        build = []
        build.extend(exp[::-1])
        build.append(start)
        build.extend(exp)
        build.append(end)
        sec.append(build)

    start = time.time()

    # Add loops at each generator
    # if computing a rack, rather than a quandle, only add the vertices
    for g in range(1,gen+1):
        Edges.append((g, g, g))
        Vertices.add(g)

    # Add the initial relations
    for rel in init:
        v1 = rel[0]
        v2 = max(Vertices)+1 # new vertex
        for w in rel[1:len(rel)-2]:
            if w > 0: # add all edges with positive labels
                Edges.append((v1, v2, w))
            else:
                Edges.append((v2, v1, -w))
            Vertices.add(v2)
            v1 = v2
            v2 = v2+1
        # add the final edge
        w = rel[len(rel)-2]
        v2 = rel[len(rel)-1]
        if w > 0:  # add all edges with positive labels
            Edges.append((v1, v2, w))
        else:
            Edges.append((v2, v1, -w))

    # Add the secondary relations to each vertex
    completed = set({})
    count = 1 # keep track of number of completed vertices

    while completed != Vertices:
        next_vertex = min(Vertices-completed)
        Vertices, Edges = add_relations(next_vertex, sec, Vertices, Edges)
        completed.add(next_vertex)
        completed.intersection_update(Vertices) # remove completed vertices that were collapsed

        if len(completed) > 50*count:
            print(len(Vertices),'*',len(completed), '*', time.time()-start, "seconds")
            count = count+1

    print(len(Vertices),'*',len(completed))
    print("runtime =", time.time()-start, "seconds")
    
    return Vertices, Edges

def generate_graph(Vertices, Edges, path, filename, count):

    Edges = [(edge[0], edge[1], ALPHABET[edge[2]-1]) for edge in Edges]

    net = Network(notebook=True)
    c = 1
    for vertex in Vertices:
        net.add_node(vertex, shape='circle', size=10, label=str(c), title='')
        c = c + 1
    for edge in Edges:
        color = 'blue'
        match edge[2]:
            case 'a':
                color = '#ff0000'
            case 'b':
                color = '#00ff00'
            case 'c':
                color = '#0000ff'
            case 'd':
                color = "#ff00ff"
        net.add_edge(edge[0], edge[1], label=edge[2], color=color, width=4)

    # net.show(os.path.join(path,'html',filename+'.html'))
    net.show(filename+'.html')

############################################
# Example: this quandle has 134 elements
############################################

#gen = 3
#init = [[1,-3,1,3,2,1,2,1,2,1,2],[1,3,1,-3,1,2,1,2,1,2,1,2],[3,2,1,3]]
#sec = [[1, 1], [2, 2], [3, 3, 3], [2,1,3,1,2,-3],[-3,1,3,1,-3,1,3,2,1,2,1,2,1,2,1,2,1,2,1,2],[1,3,1,-3,1,3,1,-3,1,-3,1,3,1,-3,1,3]]

############################################
# Example: this quandle has 52 elements
############################################

# gen=3
# init = [[1, 2, 1, 2, 1, 2, 1, 3, 1, 2, 1, 2], [1, 2, 1, 3, 2, 1, 3], [3, 1, 2, 1, 2, 1, 3, 1, 2, 1, 2, 1, 2]]
# sec = [[1, 1], [2, 2], [3, 3], 
#        [1, 2, 1, 3, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 3, 1, 2, 1, 2], 
#        [1, 2, 3, 1, 2, 1, 2, 1, 3, 2, 1, 3], 
#        [1, 2, 1, 2, 1, 3, 1, 2, 1, 2, 1, 3, 1, 2, 1, 2, 1, 3, 1, 2, 1, 2, 1, 2]]

# gen = 3
# init = [[3,1,2,1,3,1,2,1,2,1],[1,2,1,2,1,2,1,3,1,2,1,2],[3,1,2,1,2,3,1,2]]

gen = 4
# k = -2 1,1,1
# try 1 init = [[3,2,1,2,1,3,2],[3,2,3,2,1,2,1],[2,1,2,3,2,1,2,1,2,1]]
# try 2 init = [[3,2,3,2,1,2,1],[1,2,1,2,1,2,3,2,1,2],[3,2,1,2,1,3,2]]
# try 3 init = [[1,2,1,2,1,2,1,3,1,2,1,2],[3,1,2,1,2,3,1,2],[3,1,2,1,3,1,2,1,2,1]]
# init = [[1,2,1,2,1,3,1,2,1,3],[2,1,2,1,3,1,2,1,2,1,2,1],[2,1,3,2,1,2,1,3]]
# k=2 1,1,1
# init = [[1,2,1,2,1,3,1,2,1,3], [2,1,2,1,2,1,2,1,2,3,2,1,2,1,2,1,1], [2,1,3,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,3]]
# k = 0 1,1,1
# init = [[1,2,1,2,1,3,1,2,1,3],[2,1,2,3,1],[2,1,3,1,2,1,2,1,2,1,2,3]]
# k = -1 1,1,1
# init = [[1,2,1,2,1,3,1,2,1,3],[2,2,1,2,1,2,1,2,1,2,1,3,1,2,1,2,1,2,1],[2,1,3,2,1,2,1,2,1,2,1,2,1,3]]
# k = -2 : 1,1,1 : 4 gens
# init = [[1,4,1,3,1,4], [3,2,3,2,1,2,1], [3,1,4,1,2,3,2],[2,1,2,1,4]]
# k = -1 : 1,1,1 : 4 gens
init = [[4,1,3,1], [3,2,3,2,1,2,1], [3,1,2,3,2],[2,1,2,1,4]]
file_name = f'-1_111_4gen'


Vertices, Edges = q_graph(gen, init)
print(len(Vertices))
print(Vertices)
print(Edges)

# generate_graph(Vertices, Edges, os.path.join('graphs','test2Quandle'), f'test2Quandle', 0)
generate_graph(Vertices, Edges, os.path.join('graphs','test2Quandle'), file_name, 0)

