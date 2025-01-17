import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
import random


def generate_graph_with_constraints(num_vertices, num_edges, target_triangles=3):
    """
    we attempt to generate a graph with 5 edges and 3 triangles, if such a graph exists, then we have our tirnagualtion
    """
    G = nx.Graph()
    vertices = [chr(i) for i in range(65, 65 + num_vertices)] 
    G.add_nodes_from(vertices)
    all_edges = list(combinations(vertices, 2))

    if num_edges > len(all_edges):
        print("Error: More edges requested than possible for the number of vertices.")
        return None, 0
    edges = random.sample(all_edges, num_edges)
    G.add_edges_from(edges)
    
    triangles = [
        {u, v, w} 
        for u, v in G.edges()
        for w in G.neighbors(u)
        if G.has_edge(v, w) and u != v and u != w and v != w
    ]
    triangle_count = len(set(frozenset(t) for t in triangles))

    print(f"Generated edges: {G.edges()}")
    print(f"Number of triangles found: {triangle_count}")
    
    return G, triangle_count


def visualize_graph(graph):
    pos = nx.spring_layout(graph) 
    plt.figure(figsize=(6, 6))
    nx.draw(graph, pos, with_labels=True, node_color="lightblue", edge_color="black", node_size=800, font_size=15)
    plt.title("Generated Graph Visualization")
    plt.show()


vertex_counts = [3, 4, 5, 6, 7, 8, 9, 10]  # for a differnt cadrinality of a set of points we will make attempts to create the triangualation requiered
num_edges = 5  # we need to do the trianguation with 5 edges
target_triangles = 3  # we need exactly 3 triangels
for num_vertices in vertex_counts:
    for i in range(1, 3): # 3 attempt per caridnalty, could be increased
        print("\n" + "-"*50)
        graph, triangle_count = generate_graph_with_constraints(num_vertices, num_edges, target_triangles)
        visualize_graph(graph)
        if triangle_count == target_triangles:
            print(f"The graph generated {target_triangles} triangles.")
        else:
            print(f"The generated graph does not form {target_triangles} triangles.")
