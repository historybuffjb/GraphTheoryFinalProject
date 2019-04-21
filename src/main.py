"""
This is the main file. It is where our command line script runs from.
"""
from argparse import ArgumentParser
from drawing import PlanarDrawing, FileError, DirError, ConnectivityError, MaxNodesError


def main(args):
    """ This is our main function """
    obj = PlanarDrawing()
    file = args.file
    file_out = args.fileout if args.fileout is not None else None
    output = args.output
    try:
        obj.load_adj_list(file)
        obj.draw_graph(output, file_out)
    except FileError:
        print("Error: The text file is not formatted correctly. See help.")
    except DirError:
        print("Error: The output directory given does not exist. See help.")
    except ConnectivityError:
        print("Error: The input graph must be triconnected. See help.")
    except MaxNodesError:
        print("Error: The input graph must have between 3 and 100 nodes. See help.")
    except FileExistsError:
        print("Error: Filein does not exist. See help.")
    print("Program exiting...")


if __name__ == "__main__":
    PARSER = ArgumentParser(
        description=(
            "This program will produce a plane graph drawing of an input planar graph "
            "file, as long as the graph is triconnected. To read more about "
            "triconnected graphs please visit https://en.wikipedia.org/wiki/K-vertex-connected_graph"
        )
    )
    PARSER.add_argument(
        "file",
        type=str,
        nargs="?",
        help=(
            "The file containing the adjacency list of your graph. "
            "The correct format for each line is as follows and the "
            "graph must be spread across multiple lines: 1 1 1 1"
        ),
    )
    PARSER.add_argument(
        "--fileout",
        type=str,
        nargs="?",
        default="",
        help=(
            "This optional is only for file inputs. It defines the output file name "
            "of the output graph. It is an optional argument. If no name is chosen then "
            "the graph will be saved as CURRENT_TIME.png"
        ),
    )
    PARSER.add_argument(
        "output", type=str, nargs="?", help=("The directory that will contain the output(s).")
    )

    main(PARSER.parse_args())
