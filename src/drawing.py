from datetime import datetime
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt


class FileError(Exception):
    """ Used for error handling """

    pass


class DirError(Exception):
    """ Used for error handling """

    pass


class PlanarDrawing:
    """ Uses the Networkx python module and the code developed by
        Jaden Stock(ref:  https://github.com/jadenstock/Tutte-embedding) """

    def __init__(self):
        self.__graph_drawn = False
        self.__adj_list = None

    def load_adj_list(self, file):
        pass

    def load_example(self, example, num_nodes):
        pass

    @staticmethod
    def same_neighbors(graph):
        """ Creates a list of vertices in the graph which share neighbors """
        same_neighbors = []
        for neighb in graph:
            same_neighbors_u = [neighb]
            for vert in graph:
                if vert != neighb:
                    if set(graph[neighb]) == set(graph[vert]):
                        same_neighbors_u.append(vert)
            if len(same_neighbors_u) > 1:
                same_neighbors.append(same_neighbors_u)
        same_neighbors = [set(x) for x in same_neighbors]
        same = []
        for i in same_neighbors:
            if i not in same:
                same.append(i)
        same = [list(x) for x in same]
        return same

    # input: a graph in the form of a dictionary and an outter_face in the form of a
    # list of vertices.
    @staticmethod
    def __tutte_embedding(graph, outter_face):
        """ Produces a list of positions for each vertice """
        pos = {}  # a dictionary of node positions
        tmp = nx.Graph()
        for edge in outter_face:
            edge_a, edge_b = edge
            tmp.add_edge(edge_a, edge_b)
        tmp_pos = nx.spectral_layout(tmp)  # ensures that outterface is a convex shape
        pos.update(tmp_pos)
        outter_vertices = tmp.nodes()
        remaining_vertices = [x for x in graph.nodes() if x not in outter_vertices]
        size = len(remaining_vertices)
        # create the the system of equations that will determine the x and y positions of
        # remaining vertices
        a_list = [[0 for i in range(size)] for i in range(size)]
        # the elements of theses matrices are indexed by the remaining_vertices list
        b_list = [0 for i in range(size)]
        c_list = [[0 for i in range(size)] for i in range(size)]
        d_list = [0 for i in range(size)]
        for rem in remaining_vertices:
            i = remaining_vertices.index(rem)
            neighbors = graph.neighbors(rem)
            len_neighb = len([n for n in neighbors])
            a_list[i][i] = 1
            c_list[i][i] = 1
            for vertice in neighbors:
                if vertice in outter_vertices:
                    b_list[i] += float(pos[vertice][0]) / len_neighb
                    d_list[i] += float(pos[vertice][1]) / len_neighb
                else:
                    j = remaining_vertices.index(vertice)
                    a_list[i][j] = -(1 / float(len_neighb))
                    c_list[i][j] = -(1 / float(len_neighb))
        x_coord = np.linalg.solve(a_list, b_list)
        y_coord = np.linalg.solve(c_list, d_list)
        for rem in remaining_vertices:
            i = remaining_vertices.index(rem)
            pos[rem] = [x_coord[i], y_coord[i]]
        return pos

    @staticmethod
    def __get_face(graph):
        pass

    def __draw_adj(self):
        if self.__adj_list:
            for i in range(len(self.__adj_list)):
                print("[")
                for j in range(len(self.__adj_list[i])):
                    print(f" {self.__adj_list[i][j]} ")
                print("]")

    def draw_graph(self, output, name=None):
        """ Draws a plane embedding of a given graph, if planar and 3-connected """
        if self.__adj_list:
            graph = nx.from_numpy_matrix(self.__adj_list)
            is_planar, kuratowski = nx.algorithms.planarity.check_planarity(graph, True)
            if is_planar:
                # Get random face
                face = self.__get_face(graph)
                pos = self.__tutte_embedding(graph, face)
                nx.draw_networkx(graph, pos)
            else:
                print(
                    f"Sorry, the adjancy list {self.__draw_adj()} does not represent a planar "
                    "graph. Returning a Kuratowski subgraph instead..."
                )
                nx.draw_networkx(kuratowski)
            if isinstance(name) == str and "." not in name:
                plt.save(name)
            else:
                plt.save(f"{datetime.now()}.png")


# diamond1 = np.matrix(
# [[0, 1, 1, 1, 0], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [1, 0, 0, 0, 1], [0, 1, 1, 1, 0]]
# )
# G = nx.from_numpy_matrix(diamond1)
# pos = tutte_embedding(G, [(0, 1), (1, 4), (4, 3), (3, 0)])
# nx.draw_networkx(G, pos)
# plt.show()

# example = np.matrix(
# [
# [0, 1, 0, 1, 1, 0, 0, 0],
# [1, 0, 1, 0, 0, 1, 0, 0],
# [0, 1, 0, 1, 0, 0, 1, 0],
# [1, 0, 1, 0, 0, 0, 0, 1],
# [1, 0, 0, 0, 0, 1, 0, 1],
# [0, 1, 0, 0, 1, 0, 1, 0],
# [0, 0, 1, 0, 0, 1, 0, 1],
# [0, 0, 0, 1, 1, 0, 1, 0],
# ]
# )
# G = nx.from_numpy_matrix(example)
# G = nx.PlanarEmbedding(example)
# pos = tutte_embedding(G, [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 0)])
# nx.draw_networkx(G, pos)
# print(G.check_structure())
# plt.show()
