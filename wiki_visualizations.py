# -*- coding: utf-8 -*-
"""
Created on Fri Mar 06 12:07:27 2015

@author: mrinmoymaity
"""

import networkx as nx 
import numpy as np
import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pygraphviz as pgv


def user_correlations_histogram(input_gml):
    G = nx.read_gml(input_gml)
    weights = []
    for source,dest,attr in G.edges(data=True):
        weights.append(attr['weight'])
    np_weights = np.array(weights)
    print(np_weights)
#    unique, counts = np.unique(np_weights, return_counts=True)
#    hist_to_plot = np.asarray((unique, counts)).T
    draw_histogram(np_weights)
#    plt.hist(weights, bins = 50)

def draw_histogram(x):
    num_bins=100
    x1, x2 = -300, 300
    y1, y2 = 0, 70000
    # the histogram of the data
    n, bins, patches = plt.hist(x, num_bins, facecolor='green', alpha=1)
    # add a 'best fit' line
    plt.xlabel('# Agreement among Users')
    plt.ylabel('Frequencies')
    plt.title("User Agreements")
    plt.axis([x1, x2, y1, y2])

    # Tweak spacing to prevent clipping of ylabel
    plt.subplots_adjust(left=0.15)
    plt.savefig("user_correlations_hist.png")
    plt.show()

user_correlations_histogram('test_user_graph.gml')
#user_correlations_histogram('user_graph.gml')