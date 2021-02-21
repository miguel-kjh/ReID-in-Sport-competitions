import argparse
import os

from Controller.ReaderFilesController import ReaderFilesController

def faceDetection(directory, model = "retinaface", heuristic = "none"):

    rf = ReaderFilesController(heuristic, model=model)

    folders = [name for name in os.listdir(directory)]
    for folder in folders:
        rf.run(os.path.join(directory, folder))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", action='store', type=str, required=True, help="introduce the direction of folder")
    parser.add_argument("--model", action='store', type=str, required=True,  help="introduce the model")
    parser.add_argument("--heuristic",action='store', type=str, help="introduce the type of heuristic")
    args = parser.parse_args()

    if args.heuristic:
        faceDetection(args.folder, model=args.model, heuristic=args.heuristic)
    else:
        faceDetection(args.folder, model=args.model)

