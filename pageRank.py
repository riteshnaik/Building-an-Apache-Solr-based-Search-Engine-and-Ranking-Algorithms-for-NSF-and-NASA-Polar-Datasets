import sys
import pickle
import networkx as nx

def main(argv):
    graph_file = open('dump.graph', 'rb')
    pr_file = open('pr.txt','w')
    gr = pickle.load(graph_file)
    graph_file.close()
    
    print('Graph Loaded from file')

    # make new graph with sum of weights on each edge
    G = nx.Graph()
    for u,v,d in gr.edges(data=True):
        w = d['weight']
        if G.has_edge(u,v):
            G[u][v]['weight'] += w
        else:
            G.add_edge(u,v,weight=w)
    #G = nx.DiGraph(gr)
    #print('Converted to Directed Graph')
    #sys.exit()
    print('Converted Mutigraph to Simple Graph')
    pr = nx.pagerank(G, alpha=0.9, max_iter=10)
    print(len(G.nodes()))
    for n in sorted(pr, key=pr.get, reverse=True):
        pr_file.write(n +' '+str(pr[n])+'\n')
            

if __name__=="__main__":
    main(sys.argv[1:])
