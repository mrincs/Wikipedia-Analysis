# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 14:37:59 2015

@author: mrinmoymaity
"""
import networkx as nx
import numpy as np

# Input two graphs G1 and G2 
# Output G1 intersection G2
def find_overlapping_nodes(G1,G2):
    common_users = []
    if G1.number_of_nodes() > G2.number_of_nodes():
        G1, G2 = G2, G1
    for user in G1.nodes():
        if G2.has_node(user):
            common_users.append(user)
    return common_users
    
## test find_overlapping_nodes
#def test_find_overlapping_nodes():
#    G1 = nx.path_graph(10)
#    G2 = nx.tetrahedral_graph()
#    print G1.nodes()
#    print G2.nodes()
#    find_overlapping_nodes(G1, G2)
#    
#test_find_overlapping_nodes()


# Input two graphs G1 and G2 
# Output G1 s edges intersection G2 s edges   
def find_overlapping_edges(G1, G2):
    common_links = []
    if G1.number_of_edges() > G2.number_of_edges():
        G1, G2 = G2, G1
    for link in G1.edges():
        user1, user2 = link
        if G2.has_edge(user1, user2):
            common_links.append([link, G1[user1][user2]['weight']+G2[user1][user2]['weight']])
    return common_links
    
## test find_overlapping_nodes
#def test_find_overlapping_edges():
#    G1 = nx.path_graph(10)
#    G2 = nx.tetrahedral_graph()
#    print G1.edges()
#    print G2.edges()
#    find_overlapping_edges(G1, G2)
#    
#test_find_overlapping_edges()
    
def graph_union_combine_edge_weights(G1, G2):
    G = nx.Graph()
    for user in G1.nodes():
        if G.has_node(user) != None:
            G.add_node(user)
    for user in G2.nodes():
        if G.has_node(user) != None:
            G.add_node(user)
    for link in G1.edges():
        user1, user2 = link
        if G.has_edge(user1, user2) != None:
            G.add_edge(user1, user2)
            G[user1][user2]['weight'] = G1[user1][user2]['weight']
        else:
            G[user1][user2]['weight'] += G1[user1][user2]['weight']
    for link in G2.edges():
        user1, user2 = link
        if G.has_edge(user1, user2) != None:
            G.add_edge(user1, user2)
            G[user1][user2]['weight'] = G2[user1][user2]['weight']
        else:
            G[user1][user2]['weight'] += G2[user1][user2]['weight']
    return G
    
#def test_graph_union():
#    G1 = nx.Graph()
#    G1.add_weighted_edges_from([(1,5,0.125),(1,3,0.75),(2,4,1.8),(3,5,0.1)])
#    G2 = nx.Graph()
#    G2.add_weighted_edges_from([(1,2,0.125),(1,3,0.75),(2,4,1.2),(3,4,0.375)])
#    print G1.edges()
#    print G2.edges()
#    graph_union(G1, G2)
#    
#test_graph_union()
    
def graph_union_ignore_edge_weights(G1, G2):
    G = nx.Graph()
    for user in G1.nodes():
        if G.has_node(user) != None:
            G.add_node(user)
    for user in G2.nodes():
        if G.has_node(user) != None:
            G.add_node(user)
    for link in G1.edges():
        user1, user2 = link
        if G.has_edge(user1, user2) != None:
            G.add_edge(user1, user2)
    for link in G2.edges():
        user1, user2 = link
        if G.has_edge(user1, user2) != None:
            G.add_edge(user1, user2)
    return G
    
# Combine all the graph nodes and edges
# Edge weights of overlapping graph is sum of previous ones
def graph_intersection_combine_edge_weights(G1, G2):
    G = nx.Graph()
    if G1.number_of_nodes() > G2.number_of_nodes():
        G1, G2 = G2, G1
    for user in G1.nodes():
        if G2.has_node(user) and G.has_node(user) != None:
            G.add_node(user)
    if G1.number_of_edges() > G2.number_of_edges():
        G1, G2 = G2, G1
    for link in G1.edges():
        user1, user2 = link
        if G2.has_edge(user1, user2) and G.has_edge(user1, user2) != None:
            G.add_edge(user1, user2, weight=G1[user1][user2]['weight']+G2[user1][user2]['weight'])
    #print G.edges()
    return G

# Used to find out how much part of a graph contributes to overlaps
def part_in_overlapping_graph(subpart_G, overlapped_G):
    edge_set = []
    for overlapping_edge in overlapped_G.edges():
        user1, user2 = overlapping_edge
        if subpart_G.has_edge(user1, user2):            
            edge_set.append([user1, user2, subpart_G[user1][user2]['weight']])
    return edge_set

# Accept an array in form <node1, node2, weight> and return set of weights
def set_of_weights(edge_set):
    set_of_weights = []
    for idx in range(len(edge_set)):
        set_of_weights.append(edge_set[idx][2])
    return set_of_weights


# Accept arrays and return Pearson's correlation coefficient
def calculate_correlation_coeff(w1, w2):
    set1 = np.array(w1)
    set2 = np.array(w2)
    return np.corrcoef(set1, set2)[0][1]
    
    
def main():
    
    # Create two separate graphs
    G1 = nx.Graph()
    G1.add_weighted_edges_from([(1,5,0.125),(1,3,0.75),(2,4,1.8),(3,5,0.1)])
    G2 = nx.Graph()
    G2.add_weighted_edges_from([(1,2,0.125),(2,4,1.2),(1,3,0.5),(3,5,0.375)])
    
    
#    V_common = find_overlapping_nodes(G1, G2)
#    E_common = find_overlapping_edges(G1, G2)
    G_union = graph_union_combine_edge_weights(G1, G2)
    G_common = graph_intersection_combine_edge_weights(G1, G2)
    E_G1_common = part_in_overlapping_graph(G1, G_common)
    E_G2_common = part_in_overlapping_graph(G2, G_common)
    weight_A = set_of_weights(E_G1_common)
    weight_B = set_of_weights(E_G2_common)
    

    # Measure the extent of overlapping
    Jac_coef = G_common.number_of_edges()/float(G_union.number_of_edges())
    # Measure the similarity in user behavior in overlapping network
    edge_correlation = calculate_correlation_coeff(weight_A, weight_B)
    
    print "Measure of extent of overlaps:\n", Jac_coef
    print "Edge Correlation:\n", edge_correlation
    
main()