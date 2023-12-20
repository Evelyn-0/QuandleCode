import time
import math
import os
from tabulate import tabulate
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt 
from pyvis.network import Network

ALPHABET = list('abcdefghijklmnopqrstuvwxyz')


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
    net.force_atlas_2based(overlap= 1)
    net.show_buttons(filter_=["physics"])
    net.show(filename+'.html')

Vertices = {1,2,3}
Edges = [(1,2,1),(2,1,4),(1,3,2),(1,3,3)]
file_name = "nettest"

generate_graph(Vertices, Edges, "path", file_name, 0)