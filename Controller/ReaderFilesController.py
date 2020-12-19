import os
import re

from Services.FaceLocatorService import FacesLocatorService
from Services.SaveFacesJson import SaveFacesJson
from Utils.Heuristics.FaceHeuristic import FaceHeuristic
from Utils.Heuristics.HeuristicCreator import HeuristicCreator

class ReaderFilesController:
    def __init__(self):
        self.saveService: SaveFacesJson = SaveFacesJson()
        self.faceLocatorService: FacesLocatorService = FacesLocatorService()
        self.heuristicCreator: HeuristicCreator = HeuristicCreator()

    def _isImage(self, filename: str):
        return re.search(".jpg$", filename)

    def run(self, folder: str, heuristic: str = 'none') -> None:
        faceHeuristic: FaceHeuristic = self.heuristicCreator.getHeuristic(heuristic)
        for dirpath, dirnames, filenames in os.walk(folder):
            for filename in filenames:
                if self._isImage(filename):
                    facesCollection = self.faceLocatorService.locate("%s/%s" % (folder,filename))
                    self.saveService.saveFaces(folder, filename, faceHeuristic.filterFaces(facesCollection))