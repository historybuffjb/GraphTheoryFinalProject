from datetime import datetime
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from pathlib import Path


class FileError(Exception):
    """ Used for error handling """


class DirError(Exception):
    """ Used for error handling """


class NoAdjList(Exception):
    """ Used for error handling """


class ConnectivityError(Exception):
    """ Used for error handling """


class PlanarDrawing:
    """ Uses the Networkx python module and the code developed by
        Jaden Stock(ref:  https://github.com/jadenstock/Tutte-embedding) """

    def __init__(self):
        self.__graph_drawn = False
        self.__adj_list = None
        self.__graph = None

    def load_adj_list(self, file):
        """ Loads an adjacency list from a file and converts it to a networkx graph """
        if Path(file).is_file():
            try:
                self.__adj_list = np.loadtxt(file)
                self.__graph = nx.from_numpy_matrix(self.__adj_list)
                if nx.node_connectivity(self.__graph) != 3:
                    self.__adj_list = None
                    self.__graph = None
                    raise ConnectivityError
            except ValueError:
                raise FileError
        else:
            raise FileExistsError

    def __same_neighbors(self):
        """ Creates a list of vertices in the graph which share neighbors """
        same_neighbors = []
        for neighb in self.__graph:
            same_neighbors_u = [neighb]
            for vert in self.__graph:
                if vert != neighb:
                    if set(self.__graph[neighb]) == set(self.__graph[vert]):
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
    def __tutte_embedding(self, outter_face):
        """ Produces a list of positions for each vertice """
        pos = {}  # a dictionary of node positions
        tmp = nx.Graph()
        for edge in outter_face:
            edge_a, edge_b = edge
            tmp.add_edge(edge_a, edge_b)
        tmp_pos = nx.spectral_layout(tmp)  # ensures that outterface is a convex shape
        pos.update(tmp_pos)
        outter_vertices = tmp.nodes()
        remaining_vertices = [x for x in self.__graph.nodes() if x not in outter_vertices]
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
            neighbors = self.__graph.neighbors(rem)
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

    def __get_face(self):
        """ Gets an outer face to draw a planar drawing """
        return self.__same_neighbors()

    def draw_graph(self, output, name=None):
        """ Draws a plane embedding of a given graph, if planar and 3-connected """
        if self.__graph:
            nx.draw_networkx(self.__graph)
            if isinstance(name, str) and "." not in name:
                orig_name = f"{name}_orig"
                name = f"{name}"
            else:
                orig_name = f"{datetime.now}_orig"
                name = f"{datetime.now}"
            plt.savefig(f'{orig_name}.png')
            is_planar, kuratowski = nx.algorithms.planarity.check_planarity(self.__graph, True)
            if is_planar:
                # Get random face
                face = self.__get_face()
                pos = self.__tutte_embedding(face)
                nx.draw_networkx(self.__graph, pos)
            else:
                print(
                    f"The adjancy list \n{self.__adj_list}\n does not represent a planar "
                    "graph. Returning a Kuratowski subgraph instead..."
                )
                nx.draw_networkx(kuratowski)
                name = f'{name}_kuratowski'
            plt.savefig(f'{name}.png')
            self.__adj_list = None
        else:
            # This will only be used as stand-alone
            raise NoAdjList("No adjacency list. Run load_adj_list and then retry.")
