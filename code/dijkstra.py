"""
Disjsktra's Algorithm in GIS for Water Resources
By A.J. Brown, Ansley.Brown@colostate.edu

Executive Summary:
Dijkstra's algorithm is an algorithm for finding the shortest paths between 
nodes in a graph, which may represent, for example, road networks. It was 
conceived by computer scientist Edsger W. Dijkstra in 1956 and published three 
years later.

This python implementation is based on the pseudocode from geeksforgeeks.org
and allows users to input their own adjacency matrix. The adjacency matrix
should be a square matrix, and the cost of each vertex/node should be added
to the cost of each edge (see detail in dijkstra fxn).

Please look at the README.md for its usage in my homework assignment.

Cheers,
AJ
"""

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.lines import Line2D

NO_PARENT = -1

def dijkstra(adjacency_matrix, start_vertex):
    '''
    Note that this function assumes that each vertex/node has no cost
    associated with it. The cost is only associated with the edges.

    As such, you need to mannually add the cost of each vertex/node to each edge
    in the adjacency matrix. For example, if you have a graph with 3 vertices
    and 3 edges, you would have a 3x3 adjacency matrix. If the existing edge
    cost between 0 and 1 is 4, and the cost at point 1 is 5, then you would 
    need to add 5 to the edge cost to accurately represent the cost of the
    path from 0 to 1 (i.e, add 5 to the adjacency_matrix[0][1] and 
    adjacency_matrix[1][0] entries). You would then make the node cost at node
    1 0, since it has already been accounted for in the edge cost (i.e.
    adjacency_matrix[1][1] = 0).

    You can use the excel file included in this repository to help you do this.

    '''

    n_vertices = len(adjacency_matrix[0])

	# shortest_distances[i] will hold the
	# shortest distance from start_vertex to i
    shortest_distances = [sys.maxsize] * n_vertices

	# added[i] will true if vertex i is
	# included in shortest path tree
	# or shortest distance from start_vertex to
	# i is finalized
    added = [False] * n_vertices

	# Initialize all distances as
	# INFINITE and added[] as false
    for vertex_index in range(n_vertices):
        shortest_distances[vertex_index] = sys.maxsize
        added[vertex_index] = False
		
	# Distance of source vertex from
	# itself is always 0
    shortest_distances[start_vertex] = 0

	# Parent array to store shortest
	# path tree
    parents = [-1] * n_vertices

	# The starting vertex does not
	# have a parent
    parents[start_vertex] = NO_PARENT

	# Find shortest path for all
	# vertices
    for i in range(1, n_vertices):
		# Pick the minimum distance vertex
		# from the set of vertices not yet
		# processed. nearest_vertex is
		# always equal to start_vertex in
		# first iteration.
        nearest_vertex = -1
        shortest_distance = sys.maxsize
        for vertex_index in range(n_vertices):
            if not added[vertex_index] and shortest_distances[vertex_index] < shortest_distance:
                nearest_vertex = vertex_index
                shortest_distance = shortest_distances[vertex_index]

		# Mark the picked vertex as
		# processed
        added[nearest_vertex] = True

		# Update dist value of the
		# adjacent vertices of the
		# picked vertex.
        for vertex_index in range(n_vertices):
            edge_distance = adjacency_matrix[nearest_vertex][vertex_index]
            if edge_distance > 0 and shortest_distance + edge_distance < shortest_distances[vertex_index]:
                parents[vertex_index] = nearest_vertex
                shortest_distances[vertex_index] = shortest_distance + edge_distance

    print_solution(start_vertex, shortest_distances, parents)

def print_solution(start_vertex, distances, parents):
    # A utility function to print
    # the constructed distances
    # array and shortest paths
	n_vertices = len(distances)
	print("Vertex\t Distance (or Cost)\tPath")
	
	for vertex_index in range(n_vertices):
		if vertex_index != start_vertex:
			print("\n", start_vertex, "->", vertex_index, "\t", distances[vertex_index], "\t\t", end="")
			print_path(vertex_index, parents)

def print_path(current_vertex, parents):
    # Function to print shortest path
    # from source to current_vertex
    # using parents array
	# Base case : Source node has
	# been processed
	if current_vertex == NO_PARENT:
		return
	print_path(parents[current_vertex], parents)
	print(current_vertex, end=" ")

# 14 March update: added a function to find max cost path

def max_cost_path(adj_matrix):
    """
    This function finds the longest path in a directed acyclic graph (DAG).
    It uses the networkx package to create a directed graph from the adjacency
    matrix, and then uses the dag_longest_path_length function to find the
    longest path. If there is a cycle in the graph, it will return an error.
    It also creates a graph visualization using networkx and matplotlib, where
    green represents nodes selected on the longest path, and blue represents
    nodes not selected on the longest path.
    params:
        adj_matrix: a square adjacency matrix
    returns:
        None
    """
    G = ucg2dag(adj_matrix)
    try:
        path = nx.dag_longest_path(G, weight='weight')
        path_length = nx.dag_longest_path_length(G, weight='weight')
        print("The longest path is:\n", path)
        print("The total weight of the longest path is:\n", path_length)
    except nx.exception.NetworkXUnfeasible: # There's a loop!
        print("The graph has a cycle, and a longest path cannot be determined.")
    node_colors = ["green" if n in path else "blue" for n in G.nodes()]
    labels = {e: G.edges[e]['weight'] for e in G.edges}
    pos = nx.spring_layout(G, k=1)
    nx.draw_networkx(G,
                     pos=pos,
                     arrows=True, 
                     with_labels=True,
                     arrowstyle='-|>', 
                     arrowsize=20, 
                     node_size=800,
                     node_color=node_colors)
    
    nx.draw_networkx_edge_labels(G, 
                                 pos=pos,
                                 edge_labels=labels)
    legend_elements = [Line2D([0], [0], marker='o', color='w',
                              label='Optimized Path', markerfacecolor='g',
                              markersize=15),
                       Line2D([0], [0], marker='o', color='w',
                              label='Omitted Nodes', markerfacecolor='b',
                              markersize=15)]
    plt.legend(handles=legend_elements)
    plt.show()

def ucg2dag(adj_matrix):
    """
    Converts an undirected connected graph (i.e, adjacency matrix) to a directed
    acyclic graph (DAG)
    params:
        adj_matrix: adjacency matrix of the graph (numpy array)
        starts: set of starting vertices (dict)
    """
    # convert to numpy array
    adj2 = np.array(adj_matrix, dtype=np.float32)
    # fill diagonal with nans
    adj2[adj2 == 0] = np.nan
    np.fill_diagonal(adj2, np.nan)
    # convert to dataframe
    df = pd.DataFrame(adj2)
    # convert to edge list
    df = df.stack().reset_index()
    # rename columns for interpretation
    df.rename(columns={'level_0': 'source', 'level_1': 'target', 0: 'weight'}, 
              inplace=True)
    # correct node numbering for correct interpretation
    df[['source','target']] += 1
    # convert to directed acyclic graph (DAG)
    dag = nx.from_pandas_edgelist(df, 'source', 'target', 'weight',
                                  create_using=nx.Graph())
    # remove self-loops
    dag_dir = dag.to_directed()
    dropped_nodes = list(set(dag_dir.nodes()) - set(dag.nodes()))
    dropped_edges = list(set(dag_dir.edges()) - set(dag.edges()))
    dag_dir.remove_nodes_from(n for n in dropped_nodes)
    dag_dir.remove_edges_from(e for e in dropped_edges)
    '''
    #for debugging
    print(type(dag))
    print(dag.edges())
    print(type(dag_dir))
    print(dag_dir.edges())
    print('dropped edges:')
    print(dropped_edges)
    print('final edges:')
    print(dag_dir.edges())
    '''
    return dag_dir
    

# Driver code
if __name__ == '__main__':
    # adjacency matrix for homework problem 1
    print("###### Problem 1 ######")
    print("Note that directionality does not matter for this problem")
    print("i.e., the cost from 0 to 16 = the cost of 16 to 0 for all vertices")
    print("\n")
    print("Location Key for Problem 1:")
    print("0 = A1, 1 = B1, 2 = B2, 3 = B3, 4 = B4, 5 = C1, 6 = C2, 7 = C3, 8 = C4,")
    print("9 = D1, 10 = D2, 11 = D3, 12 = D4, 13 = E1, 14 = E2, 15 = E3, 16 = E4")
    print("\n")
    print("Assuming starting point at vertex: 0")
    adjacency_matrix_p1 = [[0,22,19,17,18,0,0,0,0,0,0,0,0,0,0,0,0],
                                [22,0,0,0,0,17,19,0,0,0,0,0,0,0,0,0,0],
                                [21,0,0,0,0,19,19,19,0,0,0,0,0,0,0,0,0],
                                [17,0,0,0,0,0,21,21,25,0,0,0,0,0,0,0,0],
                                [18,0,0,0,0,0,0,22,24,0,0,0,0,0,0,0,0],
                                [0,18,21,0,0,0,0,0,0,14,13,0,0,0,0,0,0],
                                [0,17,18,19,0,0,0,0,0,19,17,14,0,0,0,0,0],
                                [0,0,17,18,19,0,0,0,0,0,19,16,21,0,0,0,0],
                                [0,0,0,17,16,0,0,0,0,0,0,18,22,0,0,0,0],
                                [0,0,0,0,0,14,22,0,0,0,0,0,0,18,16,0,0],
                                [0,0,0,0,0,15,22,25,0,0,0,0,0,16,14,18,0],
                                [0,0,0,0,0,0,20,23,30,0,0,0,0,0,16,17,19],
                                [0,0,0,0,0,0,0,22,28,0,0,0,0,0,0,18,20],
                                [0,0,0,0,0,0,0,0,0,20,16,0,0,0,0,0,0],
                                [0,0,0,0,0,0,0,0,0,19,15,16,0,0,0,0,0],
                                [0,0,0,0,0,0,0,0,0,0,17,15,22,0,0,0,0],
                                [0,0,0,0,0,0,0,0,0,0,0,16,23,0,0,0,0]]
    dijkstra(adjacency_matrix_p1, 0)
    print("\n")
    # new adjacency matrix for homework problem 2
    print("###### Problem 2 ######")
    print("Note that directionality does not matter for this problem")
    print("i.e., the cost from 0 to 12 = the cost of 12 to 0 for all vertices")
    print("\n")
    print("Location Key for Problem 2:")
    print("0 = 1, 1 = 2, ..., 11 = 12,")
    print("\n")
    print("Assuming starting point at vertex: 0")
    adjacency_matrix_p2 = [[0,1,2,0,2,0,0,0,0,0,0,0],
                                [1,0,0,3,4,0,0,0,0,0,0,0],
                                [2,0,0,0,0,4,0,0,5,0,0,0],
                                [0,3,0,0,5,0,4,0,0,0,0,0],
                                [2,4,0,5,0,0,0,5,0,0,0,0],
                                [0,0,4,0,0,0,0,2,0,0,0,0],
                                [0,0,0,4,0,0,0,4,0,5,0,0],
                                [0,0,0,0,5,2,4,0,3,0,0,5],
                                [0,0,5,0,0,0,0,3,0,0,4,0],
                                [0,0,0,0,0,0,5,0,0,0,0,6],
                                [0,0,0,0,0,0,0,0,4,0,0,7],
                                [0,0,0,0,0,0,0,5,0,6,7,0]]
    dijkstra(adjacency_matrix_p2, 0)
    print("\n")
    adjacency_matrix_midterm = [[0,1,2,0,4,0,0,0,0,0,0,0],
                                [1,0,0,3,4,0,0,0,0,0,0,0],
                                [2,0,0,0,0,4,0,0,5,0,0,0],
                                [0,3,0,0,5,0,4,0,0,0,0,0],
                                [4,4,0,5,0,3,2,5,0,0,0,0],
                                [0,0,4,0,3,0,0,2,3,0,0,0],
                                [0,0,0,4,2,0,0,4,0,5,0,0],
                                [0,0,0,0,5,2,4,0,3,1,4,5],
                                [0,0,5,0,0,3,0,3,0,0,4,0],
                                [0,0,0,0,0,0,5,1,0,0,0,6],
                                [0,0,0,0,0,0,0,4,4,0,0,7],
                                [0,0,0,0,0,0,0,5,0,6,7,0]]
    #single_source_longest_dag_path_length(adjacency_matrix_midterm, 0)
    max_cost_path(adjacency_matrix_midterm)


    
