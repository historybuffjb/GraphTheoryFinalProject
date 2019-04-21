"""
This is the main file. It is where our command line script runs from.
"""
from argparse import ArgumentParser
from drawing import PlanarDrawing, FileError, DirError

MAX_NODES = 100


def main(args):
    """ This is our main function """
    obj = PlanarDrawing()
    if args.filein:
        if not args.fileout:
            raise Exception(
                "Sorry, but when you choose filein you must also choose the --fileout option."
            )
        try:
            if not obj.load_adj_list(args.filein):
                print(
                    f"It looks like {args.filein} was unable to generate a plane embedding."
                    " Are you sure that {args.filein} is an adjacency list?"
                )
            else:
                obj.draw_graph(args.output, args.fileout)
        except FileError:
            print("Sorry, you have passed ")
        except DirError:
            print("Sorry, exceptions still need to be implemented")
    elif args.example:
        if not args.numnodes:
            raise Exception(
                "Sorry, but when you choose an example graph you must also "
                "choose the --numnodes option."
            )
        if not obj.load_example(args.example, args.numnodes):
            print(
                f"It looks like {args.numnodes} is too large. The maximum number of nodes "
                "allowed is {MAX_NODES}."
            )
        else:
            obj.draw_graph(args.output)
    print("Exiting...")


if __name__ == "__main__":
    PARSER = ArgumentParser(
        description="This program will produce a plane graph drawing of an input planar graph file."
    )
    GROUP = PARSER.add_mutually_exclusive_group(required=True)
    GROUP.add_argument(
        "--filein",
        type=str,
        nargs="?",
        help=(
            "The file containing the adjacency list of your graph. "
            "The correct format is as follows and can be spread across multiple lines: "
            "[[..], [..], [..]..]"
        ),
    )
    GROUP.add_argument(
        "--example",
        type=str,
        nargs="?",
        choices=["CompleteGraph", "Random"],
        help=(
            "If you choose this option, you can choose from the list of example graphs. "
            "Just add the optional argument --numnodes N, where N is the number of nodes "
            "you would like."
        ),
    )
    PARSER.add_argument(
        "--numnodes",
        type=int,
        nargs="?",
        default=0,
        help=(
            "This optional is only for example graphs. It defines the number of nodes "
            "in the example graph."
        ),
    )
    PARSER.add_argument(
        "--fileout",
        type=str,
        nargs="?",
        default="",
        help=(
            "This optional is only for file inputs. It defines the output file name "
            "of the output graph."
        ),
    )
    PARSER.add_argument(
        "output", type=str, nargs="?", help=("The directory that will contain the output(s).")
    )

    main(PARSER.parse_args())
