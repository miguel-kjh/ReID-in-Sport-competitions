from Controller.ReaderFilesController import ReaderFilesController
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="introduce the direction of folder")
    parser.add_argument("heuristic", help="introduce the type of heuristic")
    args = parser.parse_args()
    rf = ReaderFilesController()

    rf.run(str(args.folder), str(args.heuristic))
