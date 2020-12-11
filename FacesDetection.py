from Controller.ReaderFilesController import ReaderFilesController
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="introduce the direction of folder")
    args = parser.parse_args()
    rf = ReaderFilesController()
    rf.run(str(args.folder))
