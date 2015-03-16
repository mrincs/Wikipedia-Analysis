# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 17:30:35 2015

@author: mrinmoymaity
"""

import networkx as nx
import matplotlib.pyplot as plt

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
#        print "(",user1,",",user2,") does not exist" 
        G.add_edge(user1,user2,weight=weight)       
#    print user1,user2," ",G[user1][user2]['weight']
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

def draw_wiki_graph(G):
    nx.draw_circular(G)
    plt.savefig("wikiusers.png")
    
def graph_properties(G):
    print "#######"
    print "Nodes:"
    print "====================="
    print G.nodes()
    print "Edges:"
    print "====================="
    print G.edges()
    print "Radius:", nx.radius(G)
    print "Diameter:", nx.diameter(G)
    print "Density:", nx.density(G)
    print "Periphery:", nx.periphery(G)
    
def parseRevisionFile(inputFile):
    G = initialize_wiki_graph()
    for lines in inputFile:

        if lines[0] != '#':
            words = lines.split(",")
            reverter = int(words[0].strip())
            revertedTo = int(words[1].strip())
            reverted = int(words[2].strip())
            if reverter != -1 and revertedTo != -1 and reverted != -1:
                include_in_network(G,reverter,revertedTo,reverted)
#                print reverter,revertedTo,reverted
        else:
            #New pageID
            continue
    nx.write_gml(G,'user_graph.gml')
#    graph_properties(G)
    #draw_wiki_graph(G)

def main():
    inputpath = "revision.log"
    #inputpath = "test.log"
    inputFile = open(inputpath,"r")
    parseRevisionFile(inputFile)
    inputFile.close()
    

main()    
