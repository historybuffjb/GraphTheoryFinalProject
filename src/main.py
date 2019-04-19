from argparse import ArgumentParser
from dfpp import DFPP
from pathlib import Path
from exceptions import DirError, FileError


def main(args):
    files = (
        Path(args.file[0]).glob("**/*.txt")
        if len(args.file) == 1 and Path(args.file[0]).is_dir()
        else args.file
    )
    for file in files:
        try:
            obj = DFPP(file, args.output[0])
            if not obj.generate_drawing():
                print(f"It looks like {file} was unable to generate a plane embedding.")
            else:
                print(f"Graph {file} was able to be embedded in the plane at {obj.output_path}")
        except FileError:
            print(
                f"Sorry, it looks like file {file} doesn't exist. Continuing to next file if any..."
            )
        except DirError:
            print(
                f"Sorry, it looks like output directory {args.output[0]} does not exist. Exiting..."
            )
            return


if __name__ == "__main__":
    parser = ArgumentParser(
        description="This program will produce a plane graph drawing of an input planar graph file."
    )
    parser.add_argument(
        "file",
        type=str,
        nargs="+",
        help=(
            "The file containing the edges of your graph."
            "The correct format is as follows:"
            "e1,e2 e2,e3 e20,e2..."
        ),
    )
    parser.add_argument(
        "output", type=str, nargs="+", help=("The directory that will contain all of your outputs.")
    )

    main(parser.parse_args())
