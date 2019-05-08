""" This is our graph drawing module """
from datetime import datetime
from pathlib import Path
import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
import warnings

# Matplotlib has weird warnings. Ignore all of them.
warnings.filterwarnings("ignore")


class FileError(Exception):
    """ Used for error handling """


class DirError(Exception):
    """ Used for error handling """


class NoAdjList(Exception):
    """ Used for error handling """


class ConnectivityError(Exception):
    """ Used for error handling """


class MaxNodesError(Exception):
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
                print("Loading adjacency matrix from text file...")
                self.__adj_list = np.loadtxt(file)
                print("Converting adjacency matrix to networkx graph...")
                self.__graph = nx.from_numpy_matrix(self.__adj_list)
                print("Checking that graph is triconnected...")
                if nx.node_connectivity(self.__graph) != 3:
                    self.__adj_list = None
                    self.__graph = None
                    raise ConnectivityError
                print("Checking that the number of nodes is between 3 and 100...")
                if nx.number_of_nodes(self.__graph) < 3 or nx.number_of_nodes(self.__graph) > 100:
                    raise MaxNodesError
                print("Graph successfully loaded.")
            except ValueError:
                raise FileError
        else:
            raise FileExistsError

    # input: a graph in the form of a dictionary and an outter_face in the form of a
    # list of vertices.
    def __tutte_embedding(self, outter_face):
        """ Produces a list of positions for each vertice """
        print("Creating a tutte embedding of the graph...")
        # a dictionary of node positions
        pos = {}
        tmp = nx.Graph()
        print(self.__graph.edges())
        print(outter_face)
        for edge in outter_face:
            edge_a, edge_b = edge
            tmp.add_edge(edge_a, edge_b)
        # ensures that outterface is a convex shape
        tmp_pos = nx.spectral_layout(tmp)
        print("Check: outer face is of convex shape...")
        pos.update(tmp_pos)
        outter_vertices = tmp.nodes()
        remaining_vertices = [x for x in self.__graph.nodes() if x not in outter_vertices]
        size = len(remaining_vertices)
        # create the the system of equations that will determine the x and y positions of
        # remaining vertices
        print("Creating system of linear equations...")
        a_list = [[0 for i in range(size)] for i in range(size)]
        # the elements of theses matrices are indexed by the remaining_vertices list
        b_list = [0 for i in range(size)]
        c_list = [[0 for i in range(size)] for i in range(size)]
        d_list = [0 for i in range(size)]
        print("Get coordinates of all nodes...")
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
        print("Tutte embedding succesfully created.")
        return pos

    def __get_face(self):
        """
        Gets an outer face to draw a planar drawing.
        """
        dir_graph = self.__graph.to_directed()
        unrefined_cycles = list(nx.simple_cycles(dir_graph))
        refined_cycles = self.__create_cycle_tuples(unrefined_cycles)
        periph_cycle = None
        for cycle in refined_cycles:
            if self.__remove_edges(dir_graph, cycle):
                periph_cycle = cycle
                break
        # Naively we are assuming that since it got this far we can find an
        # outter face
        return periph_cycle

    @staticmethod
    def __create_cycle_tuples(cycles):
        """
        Given a table of networkx cycles, create an array of tuples for each cycle
        """
        result = []
        for cycle in cycles:
            temp = []
            for k, node in enumerate(cycle):
                temp.append(tuple((cycle[k - 1], node)))
            result.append(temp)
        return result

    @staticmethod
    def __remove_edges(dir_graph, cycle):
        """
        Removes the cycle from the graph, and then checks if graph is still connected.
        If it is, we have found a peripheral cycle. Return True. If none found return false.
        """
        edges = []
        temp = dir_graph
        for edge in cycle:
            temp.remove_edge(*edge)
        if nx.is_connected(temp.to_undirected()):
            return True
        return False

    def __package_cycle(self, cycle):
        """
        Takes an input cycle and returns a list of tuples defining edges of the cycle
        """
        exit()

    def draw_graph(self, output, name=None):
        """ Draws a plane embedding of a given graph, if planar and 3-connected """
        if Path(output).is_dir():
            print("Starting to embed the graph...")
            if self.__graph:
                nx.draw_networkx(self.__graph)
                if name and isinstance(name, str) and "." not in name:
                    orig_name = Path(output) / Path(f"{name}_orig")
                    name = Path(output) / Path(f"{name}")
                else:
                    orig_name = Path(output) / Path(f"{datetime.now()}_orig")
                    name = Path(output) / Path(f"{datetime.now()}")
                print(f"Creating original graph image at {orig_name}.png...")
                plt.savefig(f"{orig_name}.png")
                print("Checking graph planarity...")
                is_planar, kuratowski = nx.algorithms.planarity.check_planarity(self.__graph, True)
                if is_planar:
                    print("Graph is planar. Continuing...")
                    # Get random face
                    face = self.__get_face()
                    pos = self.__tutte_embedding(face)
                    print("Drawing graph in the plane...")
                    nx.draw_networkx(self.__graph, pos)
                else:
                    print(
                        f"The adjancy list \n{self.__adj_list}\n does not represent a planar "
                        "graph. Returning a Kuratowski subgraph instead..."
                    )
                    nx.draw_networkx(kuratowski)
                    name = f"{name}_kuratowski"
                print(f"Creating new graph image at {name}.png...")
                plt.savefig(f"{name}.png")
                self.__adj_list = None
            else:
                # This will only be used as stand-alone
                raise NoAdjList("Error: No adjacency list. Run load_adj_list and then retry.")
            print("Embedding complete.")
        else:
            raise DirError


if __name__ == "__main__":
    obj = PlanarDrawing()
    obj.load_adj_list("/home/johnathan/Documents/GraphTheoryFinalProject/tests/test-cube.txt")
    obj.draw_graph("/home/johnathan/Documents/GraphTheoryFinalProject/tests/pictures/", "cube")
