import argparse
import os

from Controller.ReaderFilesController import ReaderFilesController
from Controller.FacesRecognitionsController import FacesRecognitionsController
from Controller.FaceClippingController import FaceClippingController

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="introduce the direction of folder")
    parser.add_argument("heuristic", help="introduce the type of heuristic")
    args = parser.parse_args()
    rf = ReaderFilesController(str(args.heuristic), model='img2pose')

    directory = str(args.folder)
    folders = [name for name in os.listdir(directory)]
    folders.sort(key = lambda folder: int(folder))
    for index, folder in enumerate(folders):
        if index == 4:
            break
        rf.run(os.path.join(directory, folder))

def indentification():
    rs = FacesRecognitionsController()
    print(rs.identificationPeople("data/data_base_faces"))

def test_cliping():
    fc = FaceClippingController()
    directory = "data/TGC2020v0.3_json_retinaface_none"
    folders = [name for name in os.listdir(directory)]
    folders.sort(key = lambda folder: int(folder))
    for index, folder in enumerate(folders):
        if index == 4:
            break
        fc.getImageClippings(os.path.join(directory, folder), "")

if __name__ == '__main__':
    #main()
    #indentification()
    test_cliping()

