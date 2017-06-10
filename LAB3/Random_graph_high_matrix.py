import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

class Topology(object, nx.Graph):

    N = 20
    delta = 4
    nodes = range(N)
    np.random.seed(5)
    degree = [delta for i in xrange(N)]
    G = nx.directed_havel_hakimi_graph(degree, degree)
    G = nx.DiGraph(G)

    bb = nx.edge_betweenness_centrality(G, normalized=False)
    nx. set_edge_attributes(G, 'weight', bb)
    nx.set_edge_attributes(G, 'capacity', bb)

    T_matrix = np.zeros((N, N))

    for s in nodes:
        for d in nodes:
            if s != d:
                p = np.random.uniform(0.0,1.0)
                if p <= 0.1:
                    flow_high = np.random.uniform(5.0, 15.0)
                    T_matrix[s, d] = flow_high
                else:
                    flow_low = np.random.uniform(0.5, 1.5)
                    T_matrix[s, d] = flow_low
                if G.has_edge(s, d):
                    G.edge[s][d]['weight']= T_matrix[s,d]
                    G.edge[s][d]['capacity'] = np.random.randint(8, 12)

    f_value = 0
    (p, a) = (0, 0)
    for i in range(N):
        for j in range(N):
            edges = nx.shortest_path(G, i, j, weight='weight')
            for k in range(len(edges) - 1):
                G.edge[edges[k]][edges[k+1]]['weight'] += T_matrix[i][j]
        if i != j:
            flow_value = nx.maximum_flow_value(G, i, j)
            if flow_value > f_value:
                f_value = flow_value
                (p, a) = (i, j)

    fmax = 0
    (s_f, d_f) = (0, 0)

    for s in G.edge:
        for d in G.edge[s]:
            if G.edge[s][d]['weight'] > fmax:
                fmax = G.edge[s][d]['weight']
                (s_f, d_f) = (s, d)

    tot_edges = G.number_of_edges()

    np.set_printoptions(precision=3)
    print T_matrix
    print tot_edges
    print 'max flow value on capacity', flow_value, 'on',(p, a), 'and max flow on weight', fmax, 'on', (s_f, d_f)

    nx.draw_networkx(G, arrows=True, with_labels=True)
    plt.show()