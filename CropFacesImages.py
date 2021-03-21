import os
import argparse
from Controller.FaceClippingController import FaceClippingController

TGC = "data/TGC_places"

def testCliping(directory):
    fc = FaceClippingController(directory)
    fc.getImageClippings(TGC)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action='store', type=str, required=True, help="introduce the direction of json file")
    args = parser.parse_args()
    testCliping(args.json)