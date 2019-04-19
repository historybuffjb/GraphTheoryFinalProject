""" To be determined """

from pathlib import Path
from graph import Graph
from exceptions import DirError, FileError


class DFPP:
    """ class used to generate a planar drawing of a graph """

    def __init__(self, file, output):
        """ init function for DFPP """
        self.__graph = self.__create_graph(file)
        self.__output_path = self.__verify_output(output)

    def __create_graph(self, file):
        """ Generates a graph from a given file """
        if Path(file).is_file():
            graph = Graph()
            with open(file, "r") as f:
                for row in f.readlines():
                    for edge in row.replace("\n", "").split(" "):
                        graph.add_edge(tuple(edge.split(",")))
        else:
            raise FileError
        return graph

    def __verify_output(self, output):
        """
        Checks that the output directory exists and if it does, sets
        the output path.
        """
        if Path(output).is_dir():
            return output
        else:
            raise DirError

    def generate_drawing(self):
        """
        Using the Fraysseix, Pach and Pollack algorithm, this function
        goes through the following four stages:
        1. The graph is tested for planarity, and if it is planar a
        topological embedding is returned from the graph. Otherwise,
        a Kuratowski subgraph is returned.
        2. A canonical ordering of the input graph is computed from the
        topological embedding.
        3. The vertices are added one at a time according to the canonical
        ordering, and for each added vertex vk, vk's y-coordinate and x-offset
        updates the x-offset of wq, and possibly wq+1.
        4. The graph is traversed starting from v1 and the final x-coordinates
        are computed of the vertices by accumulating offsets.
        """
        graph = self.__boyer_myrvold_planar_test()
        can_order = self.__generate_can_ordering(graph)
        grid_graph = self.__add_vertices(can_order)
        return self.__generate_final_graph(grid_graph)

    def __boyer_myrvold_planar_test(self):
        """
        Using the Boyer and Myrvold planarity test algorithm, the graph
        is tested for planarity. If it is found to be planar a topological
        embedding of the graph is returned, otherwise a kuratowski subgraph
        is returned.
        """
        print(self.__graph.num_vertices())
        print(self.__graph.num_edges())
        return 0

    def __generate_can_ordering(self, graph):
        """ generates the canonical ordering of a given graph """
        print(graph)
        return 0

    def __add_vertices(self, ordering):
        """ given a canonical ordering, computes the y and x-offset of each v """
        print(ordering)
        return 0

    def __generate_final_graph(self, grid):
        """ generates the final x,y coordinates of each vertex of the graph """
        print(grid)
        return 0


if __name__ == "__main__":
    TEST = DFPP("test.txt")
    TEST.generate_drawing()
