import os
import argparse
from Controller.FaceClippingController import FaceClippingController

TGC = "data/TGC2020v0.3_PRL"

def testCliping(directory):
    folders = [name for name in os.listdir(directory)]
    folders.sort(key = lambda folder: int(folder))
    fc = FaceClippingController(directory)
    fc.getImageClippings(TGC)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action='store', type=str, required=True, help="introduce the direction of json file")
    args = parser.parse_args()
    testCliping(args.json)