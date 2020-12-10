from Services.FaceLocatorService import FacesLocatorService
from Services.SaveFacesJson import SaveFacesJson
import argparse


class ReaderFiles:
    def __init__(self):
        self.saveService: SaveFacesJson = SaveFacesJson()
        self.faceLocatorService: FacesLocatorService = FacesLocatorService()

    def run(self, folder: str) -> None:
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="introduce the direction of folder")
    args = parser.parse_args()
    print(args.folder)
