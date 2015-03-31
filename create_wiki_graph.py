# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 17:30:35 2015

@author: mrinmoymaity
"""

import networkx as nx

def initialize_wiki_graph():
    G = nx.Graph()
    return G

#Add Nodes/Users if not already present
def update_users(G,user):
    if G.has_node(user) != None:
        G.add_node(user)
    return

#Update weights of the edges or add one if not already present 
def update_user_links(G,user1,user2,weight):
    if G.has_edge(user1,user2):
        G[user1][user2]['weight']+=weight
    else:
        G.add_edge(user1,user2,weight=weight)       
    return

#Update user network
def include_in_network(G,reverter,revertedTo,reverted):
    update_users(G,reverter)
    update_users(G,reverted)
    update_users(G,revertedTo)
    update_user_links(G,reverter,reverted,-1)
    update_user_links(G,reverter,revertedTo,1)
#    update_user_links(G,reverted,revertedTo,-1)
    return
    
#def graph_properties(G):
#    print "#######"
#    print "Nodes:"
#    print "====================="
#    print G.nodes()
#    print "Edges:"
#    print "====================="
#    print G.edges()
#    print "Radius:", nx.radius(G)
#    print "Diameter:", nx.diameter(G)
#    print "Density:", nx.density(G)
#    print "Periphery:", nx.periphery(G)
    
def parseRevisionFile(inputFile):
    G = initialize_wiki_graph()
    for lines in inputFile:

        if lines[0] != '#':
            words = lines.split(",")
            reverter = int(words[0].strip())
            revertedTo = int(words[1].strip())
            reverted = int(words[2].strip())
            #if reverter != -1 and revertedTo != -1 and reverted != -1:
            include_in_network(G,reverter,revertedTo,reverted)
#                print reverter,revertedTo,reverted
        else:
            #New pageID
            continue
#    nx.write_gml(G,'United_States.gml')
    structural_balance(G)
#    graph_properties(G)


def structural_balance(G):

    node_list = []
    errors = 0
    balanced_triplets = 0
    unbalanced_triplets = 0
    unbalanced_triplets_all_negatives = 0
    unbalanced_triplets_one_negative = 0
    
    for node in G.nodes():
        node_list.append(node)
    for i in range(len(node_list)):
        for j in range(len(node_list)):
            for k in range(len(node_list)):
                node_A = node_list[i]
                node_B = node_list[j]
                node_C = node_list[k]
                if (i!=j) and (j!=k) and (i!=k):
                    if G.has_edge(node_A,node_B) and G.has_edge(node_B, node_C) and G.has_edge(node_C, node_A):
                            edge_AB = (G[node_A][node_B]['weight']>=0)
                            edge_BC = (G[node_B][node_C]['weight']>=0)
                            edge_CA = (G[node_C][node_A]['weight']>=0)
                            if (edge_AB and edge_BC and edge_CA) or (edge_AB + edge_BC + edge_CA == 1):
                                balanced_triplets += 1
                            elif (edge_AB + edge_BC + edge_CA == 0):
                                unbalanced_triplets += 1
                                unbalanced_triplets_all_negatives += 1
                            elif (edge_AB + edge_BC + edge_CA == 2):
                                unbalanced_triplets += 1
                                unbalanced_triplets_one_negative += 1
                            else:
                                errors += 1
   
    print "Total number of Nodes:", len(node_list)
    print "Total number of Edges:", G.number_of_edges()
    print "Maximum possible Edges:", ((len(node_list))*(len(node_list)-1)*(len(node_list)-2)/6)
    print "Edge Density:", (G.number_of_edges()*6.0/((len(node_list))*(len(node_list)-1)*(len(node_list)-2)))
    print "balanced_triplets:",balanced_triplets
    print "unbalanced_triplets:",unbalanced_triplets
    print "unbalanced_triplets_all_negatives:",unbalanced_triplets_all_negatives
    print "unbalanced_triplets_one_negative:",unbalanced_triplets_one_negative
    print "errors:",errors


def main():
    files = ["Anarchism","Christianity","Circumcision","George_W._Bush","Global_warming","Jesus","LWWEe","Muhammad","United_States"]
    for idx in range(len(files)):
        print files[idx]
        print "---------------"
        inputpath = "C:\WikiProject\Controversial Pages Single\Revision Logs\\"+files[idx]+".log"
        #inputpath = "test.log"
        inputFile = open(inputpath,"r")
        parseRevisionFile(inputFile)
        inputFile.close()
    

main()    
