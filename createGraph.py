'''from pygraph.classes.graph import graph
from pygraph.algorithms.searching import depth_first_search
gr = graph()
# Add nodes
gr.add_nodes(['X','Y','Z'])
gr.add_nodes(['A','B','C'])
# Add edges
gr.add_edge(('X','Y'))
gr.add_edge(('X','Z'))
gr.add_edge(('A','B'))
gr.add_edge(('A','C'))
gr.add_edge(('Y','B'))
# Depth first search rooted on node X
st, pre, post = depth_first_search(gr, root='X')
# Print the spanning tree
print st'''
from pygraph.classes.graph import graph
import sys
import re
import networkx as nx
import matplotlib.pyplot as plt
import pickle

def main(argv):
    input = open('test.txt', 'r')
    output = open('link.txt','w')
    edges = open('edges.txt','w')
    features = {}
    nodes = []
    for line in input:
        list = line.split(',')
        if len(features) > 800:
            break
        if len(list) > 1:
            nodes.extend([list[1]])
            if len(list) == 3 and len(list[2]) > 1 :
                feature_list = list[2].strip().split(' > ')
                for feature in feature_list:
                    if feature not in features:
                        features[feature] = []
                        features[feature].extend([list[1]])
                    else:
                        features[feature].extend([list[1]])      
    print(len(features))
    print(len(nodes))
    #print(nodes[1])
    '''for key,value in features.items():
        output.write(key+':\n')
        for link in value:
            output.write('\t'+link+'\n')'''
    #gr = graph()
    gr=nx.MultiGraph()
    gr.add_nodes_from(nodes)
    print(len(gr.nodes()))
    print(len(features))
    count = 1
    for key,value in features.items():
        print(count)
        count += 1
        edges.write(str(len(value)))
        if len(value) < 6000:
            for i in range(len(value)):
                for j in range(i+1,len(value)):
                    #edges.write(str(i)+' '+str(j)+'\n')
                    #if (value[i],value[j]) not in gr.edges():
                    gr.add_edge(value[i],value[j],weight=1,label=key)
            '''if len(value) > 1:
                sys.exit()'''
    print(len(gr.nodes()))
    print(len(gr.edges()))
    graph_dump = open('dump.graph', 'wb')
    pickle.dump(gr, graph_dump)
    graph_dump.close()
    '''nx.draw(gr)
    plt.savefig("graph.png") # save as png
    plt.show() # display'''

if __name__=="__main__":
    main(sys.argv[1:])
