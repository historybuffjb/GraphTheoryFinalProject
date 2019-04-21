import planarity
import networkx as nx
import matplotlib.pyplot as plt


G = nx.complete_graph(4)
print(planarity.is_planar(G))
print(planarity.ascii(G))
planarity.draw(G)
plt.axis("off")
plt.savefig("k4.png")








# G = nx.wheel_graph(10)
# planarity.draw(G)
# plt.axis("off")
# plt.savefig("wheel.png")

# # Ascii
# import planarity

# # Example of the complete graph of 5 nodes, K5
# # K5 is not planar

# # use text strings as labels
# edgelist = [
    # ("a", "b"),
    # ("a", "c"),
    # ("a", "d"),
    # ("a", "e"),
    # ("b", "c"),
    # ("b", "d"),
    # ("b", "e"),
    # ("c", "d"),
    # ("c", "e"),
    # ("d", "e"),
# ]

# # remove an edge
# edgelist.remove(("a", "b"))
# # graph is now planar
# # make text drawing
# print(planarity.ascii(edgelist))

# # formats
# import planarity

# # Example of the complete graph of 5 nodes, K5
# # K5 is not planar
# # any of the following formats can bed used for representing the graph

# edgelist = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]

# dictofdicts = {
    # 0: {1: {}, 2: {}, 3: {}, 4: {}},
    # 1: {2: {}, 3: {}, 4: {}},
    # 2: {3: {}, 4: {}},
    # 3: {4: {}},
    # 4: {},
# }

# dictofsets = {0: set([1, 2, 3, 4]), 1: set([2, 3, 4]), 2: set([3, 4]), 3: set([4]), 4: set([])}

# dictoflists = {
    # 0: list([1, 2, 3, 4]),
    # 1: list([2, 3, 4]),
    # 2: list([3, 4]),
    # 3: list([4]),
    # 4: list([]),
# }

# print(planarity.is_planar(edgelist))  # False
# print(planarity.is_planar(dictofdicts))  # False
# print(planarity.is_planar(dictofsets))  # False
# print(planarity.is_planar(dictoflists))  # False

# # Kuratowski
# import planarity

# # Example of the complete graph of 5 nodes, K5
# # K5 is not planar

# # use text strings as labels
# edgelist = [
    # ("a", "b"),
    # ("a", "c"),
    # ("a", "d"),
    # ("a", "e"),
    # ("b", "c"),
    # ("b", "d"),
    # ("b", "e"),
    # ("c", "d"),
    # ("c", "e"),
    # ("d", "e"),
# ]

# print(planarity.is_planar(edgelist))  # False
# # print forbidden Kuratowski subgraph (K5)
# print(planarity.kuratowski_edges(edgelist))

# # remove an edge
# edgelist.remove(("a", "b"))
# # graph is now planar
# print(planarity.is_planar(edgelist))  # True
# # no forbidden subgraph, empty list returned
# print(planarity.kuratowski_edges(edgelist))

# # network draw
# import planarity
# import networkx as nx
# import matplotlib.pyplot as plt

# G = nx.wheel_graph(10)
# planarity.draw(G)
# plt.axis("off")
# plt.savefig("wheel.png")

# # networkx interface
# import planarity
# import networkx as nx

# # Example of the complete graph of 5 nodes, K5
# G = nx.complete_graph(5)
# # K5 is not planar
# print(planarity.is_planar(G))  # False
# # find forbidden Kuratowski subgraph
# K = planarity.kuratowski_subgraph(G)
# print(K.edges())  # K5 edges

# # Pgraph class
# import planarity

# # Example of the complete graph of 5 nodes, K5
# # K5 is not planar
# # any of the following formats can bed used for representing the graph

# edgelist = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
# P = planarity.PGraph(edgelist)
# print(P.nodes())  # indexed from 1..n
# print(P.mapping())  # the node mapping
# print(P.edges())  # edges
# print(P.is_planar())  # False
# print(P.kuratowski_edges())

# edgelist.remove((0, 1))
# P = planarity.PGraph(edgelist)
# print(P.ascii())

# # Write adj list
# import planarity

# # Example of the complete graph of 5 nodes, K5
# # K5 is not planar

# # use text strings as labels
# edgelist = [
    # ("a", "b"),
    # ("a", "c"),
    # ("a", "d"),
    # ("a", "e"),
    # ("b", "c"),
    # ("b", "d"),
    # ("b", "e"),
    # ("c", "d"),
    # ("c", "e"),
    # ("d", "e"),
# ]

# # write adjlist to file in "planarity adjlist" format
# planarity.write(edgelist, "k5.adjlist")
# # nodes are mapped to integers from 1 to n
# # get mapping
# print(planarity.mapping(edgelist))
