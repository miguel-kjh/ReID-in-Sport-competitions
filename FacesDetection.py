from Controller.ReaderFilesController import ReaderFilesController
from Controller.FacesRecognitionsController import FacesRecognitionsController

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="introduce the direction of folder")
    parser.add_argument("heuristic", help="introduce the type of heuristic")
    args = parser.parse_args()
    rf = ReaderFilesController()

    rf.run(str(args.folder), str(args.heuristic))

def indentification():
    rs = FacesRecognitionsController()
    print(rs.identificationPeople("data/data_base_faces"))

if __name__ == '__main__':
    #main()
    indentification()

