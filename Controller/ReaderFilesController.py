import os
import re

from Services.FaceLocatorService import FacesLocatorService
from Services.SaveFacesJson import SaveFacesJson
from Utils.Heuristics.DimensionBasedHeuristic import DimensionBasedHeuristic

class ReaderFilesController:
    def __init__(self):
        self.saveService: SaveFacesJson = SaveFacesJson()
        self.faceLocatorService: FacesLocatorService = FacesLocatorService()
        self.heuristic: DimensionBasedHeuristic = DimensionBasedHeuristic()

    def _isImage(self, filename: str):
        return re.search(".jpg$", filename)

    def run(self, folder: str) -> None:
        for dirpath, dirnames, filenames in os.walk(folder):
            for filename in filenames:
                if self._isImage(filename):
                    facesCollection = self.faceLocatorService.locate("%s/%s" % (folder,filename))
                    self.saveService.saveFaces(folder, filename, facesCollection)