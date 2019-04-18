""" A Python Class
  File "<stdin>", line 1
    A simple Python graph class, demonstrating the essential
           ^
SyntaxError: invalid syntax facts and functionalities of graphs.  """


class Graph:
    """ The main graph class that will be used in this project """

    def __init__(self, graph_dict=None):
        """ initializes a graph object
            If no dictionary or None is given,
            an empty dictionary will be used
        """
        if graph_dict is None:
            graph_dict = {}
        self.__graph_dict = graph_dict
        self.__num_vertices = 0
        self.__num_edges = 0

    def vertices(self):
        """ returns the vertices of a graph """
        return list(self.__graph_dict)

    def num_vertices(self):
        """ returns the number of vertices of a graph """
        return self.__num_vertices

    def edges(self):
        """ returns the edges of a graph """
        return self.__generate_edges()

    def num_edges(self):
        """ returns the number of edges of a graph """
        return self.__num_edges

    def add_vertex(self, vertex):
        """ If the vertex "vertex" is not in
            self.__graph_dict, a key "vertex" with an empty
            list as a value is added to the dictionary.
            Otherwise nothing has to be done.
        """
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []
            self.__num_vertices += 1

    def add_edge(self, edge):
        """ assumes that edge is of type set, tuple or list;
            between two vertices can be multiple edges!
        """
        edge = set(edge)
        (vertex1, vertex2) = tuple(edge)
        if vertex1 in self.__graph_dict:
            self.__graph_dict[vertex1].append(vertex2)
        else:
            self.__graph_dict[vertex1] = [vertex2]
            self.__num_vertices += 1
        if vertex2 in self.__graph_dict:
            self.__graph_dict[vertex2].append(vertex1)
        else:
            self.__graph_dict[vertex2] = [vertex1]
            self.__num_vertices += 1
        self.__num_edges += 1

    def __generate_edges(self):
        """ A static method generating the edges of the
            graph "graph". Edges are represented as sets
            with one (a loop back to the vertex) or two
            vertices
        """
        edges = []
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self.__graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res
