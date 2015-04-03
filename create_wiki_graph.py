# -*- coding: utf-8 -*-
"""
Created on Fri Feb 20 17:30:35 2015

@author: mrinmoymaity
"""

import networkx as nx
import os

def path_extraction(file, level):
    dir_level_1 = os.path.dirname(file)
    dir_level_2 = os.path.dirname(dir_level_1)
    dir_level_3 = os.path.dirname(dir_level_2)
    if (level == 1):
        return dir_level_1
    elif level == 2:
        return dir_level_2
    elif dir_level_3:
        return dir_level_3
## Test path_extraction
#def test_path_extraction():
#    file = "C:\WikiProject\Controversial Single Pages Simple Wiki\Anonymous Inclusion Without Details\User Graphs With Anonymous"
#    result = path_extraction(file,3)
#    print file
#    print result
#    
#test_path_extraction()

def filename_extraction(file):
    filename = os.path.basename(file)
    parts = filename.split(".")
    return parts[0]
## Test filename extractor    
#def test_filename_extraction():
#    file = "C:\WikiProject\Controversial Single Pages Simple Wiki\Anonymous Inclusion Without Details\User Graphs With Anonymous\\abc.txt"
#    result = filename_extraction(file)
#    print file
#    print result
#test_filename_extraction()


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

#Only add edges at least one of whose end is anonymous
def update_user_links_only_anonymous(G,user1,user2,weight):
    if G.has_edge(user1,user2):
        G[user1][user2]['weight']+=weight
    else:
        if is_anonymous(user1) or is_anonymous(user2):
            update_users(G, user1)
            update_users(G, user2)
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
    
    
#Update user network only anonymous
def include_in_network_only_anonymous(G,reverter,revertedTo,reverted):
    update_user_links_only_anonymous(G,reverter,reverted,-1)
    update_user_links_only_anonymous(G,reverter,revertedTo,1)
    return
    
def graph_properties(G):
    structural_balance(G)
#    print "Radius:", nx.radius(G)
#    print "Diameter:", nx.diameter(G)
#    print "Density:", nx.density(G)
#    print "Periphery:", nx.periphery(G)


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


# Entry Function: Reads revision file containing list of reverts
# in *.log format, parse it and create an  undirected graph. Output is saved 
# in *.gml format 
def parseRevisionFile(path, inputFile):
    op_path = path_extraction(path, 2)+"\User Graphs With Anonymous\\"+filename_extraction(path)+".gml"
#    primary_op_dir = "C:\WikiProject\\"
##    internal_op_dir_anonymous_inclusion_without_details = "Controversial Single Pages Simple Wiki\Anonymous Inclusion Without Details\User Graphs With Anonymous\\"
#    internal_op_dir_anonymous_inclusion_with_IP = "Controversial Single Pages Simple Wiki\Anonymous Inclusion With IP Address\User Graphs With Anonymous\\"
#    working_op_dir = internal_op_dir_anonymous_inclusion_with_IP
    
    G = initialize_wiki_graph()
    
    
    for lines in inputFile:
        if lines[0] != '#':
            words = lines.split(",")
#            reverter = int(words[0].strip())
#            revertedTo = int(words[1].strip())
#            reverted = int(words[2].strip())
            reverter = words[0].strip()
            revertedTo = words[1].strip()
            reverted = words[2].strip()
            #if reverter != -1 and revertedTo != -1 and reverted != -1:
            include_in_network(G,reverter,revertedTo,reverted)
#                print reverter,revertedTo,reverted
        else:
            #New pageID
            continue
    nx.write_gml(G, op_path)
#    nx.write_gml(G,primary_op_dir+working_op_dir+op_filename+".gml")
    graph_properties(G)

# Test if the input is a real user_id or anonymous
def is_anonymous(num):
    try:
        int(num)
        return False
    except ValueError:
        return True
        
## Test is_anonymous
#def test_is_anonymous():
#    result = is_anonymous(45)
#    print result
#test_is_anonymous()

def parseRevisionFileOnlyAnonymous(path, inputFile):
    op_path = path_extraction(path, 2)+"\User Graphs With Anonymous\\"+filename_extraction(path)+".gml"

    G = initialize_wiki_graph()
    
    
    for lines in inputFile:
        if lines[0] != '#':
            words = lines.split(",")
            reverter = words[0].strip()
            revertedTo = words[1].strip()
            reverted = words[2].strip()
            include_in_network_only_anonymous(G,reverter,revertedTo,reverted)
        else:
            #New pageID
            continue
    nx.write_gml(G,op_path)
#    graph_properties(G)



def main():
    controversial_articles = ["Anarchism","Christianity","Circumcision","George_W._Bush","Global_warming","Jesus","LWWEe","Muhammad","United_States"]
    primary_ip_dir = "C:\WikiProject\\"
#    internal_ip_dir_anonymous_inclusion_without_details = "Controversial Single Pages Simple Wiki\Anonymous Inclusion Without Details\Revision Logs\\"
#    internal_ip_dir_anonymous_inclusion_with_IP = "Controversial Single Pages Simple Wiki\Anonymous Inclusion With IP Address\Revision Logs\\"
    input_ip_dir_only_anonymous = "Controversial Single Pages Simple Wiki\Only Anonymous\Revision Logs\\"
    working_ip_dir = input_ip_dir_only_anonymous
   
    for idx in range(len(controversial_articles)):
        print controversial_articles[idx]
        print "---------------"
        inputpath = primary_ip_dir+working_ip_dir+controversial_articles[idx]+".log"
        inputFile = open(inputpath,"r")
        parseRevisionFileOnlyAnonymous(inputpath, inputFile)
#        parseRevisionFile(inputFile,controversial_articles[idx])
        inputFile.close()


main()