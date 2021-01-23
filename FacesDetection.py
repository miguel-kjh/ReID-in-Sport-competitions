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
    print(rs.identificationPeople("data/Gallery_faces_retinaface_none"))

def test_cliping():
    directory = "data/TGC2020v0.3_json_img2pose_none"
    folders = [name for name in os.listdir(directory)]
    folders.sort(key = lambda folder: int(folder))
    fc = FaceClippingController(directory)
    for index, folder in enumerate(folders):
        if index == 4:
            break
        fc.getImageClippings("data/TGC2020v0.3_PRL")

if __name__ == '__main__':
    main()
    indentification()
    #test_cliping()

