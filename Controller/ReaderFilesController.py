import os
import re
import shutil

from Services.FaceLocatorService import FacesLocatorService
from Services.SaveFacesJson import SaveFacesJson
from Services.SaveFacesJpg import SaveFacesJpg
from Utils.Heuristics.FaceHeuristic import FaceHeuristic
from Utils.Heuristics.HeuristicCreator import HeuristicCreator

class ReaderFilesController:
    def __init__(self):
        self.saveService: SaveFacesJson = SaveFacesJson()
        self.saveServiceJpg: SaveFacesJpg = SaveFacesJpg()
        self.faceLocatorService: FacesLocatorService = FacesLocatorService()
        self.heuristicCreator: HeuristicCreator = HeuristicCreator()

        self.facesFolder: str = "cropped_faces"

    def _isImage(self, filename: str):
        return re.search("000.jpg$", filename)

    def _moveFaces(self, folder: str) -> None:
        folder = "%s/%s" %(folder, self.facesFolder)
        if os.path.exists(folder): shutil.rmtree(folder)
        os.mkdir(folder)

        for f in self.saveServiceJpg.files:
            shutil.move(f, folder)

    def run(self, folder: str, heuristic: str = 'none') -> None:
        faceHeuristic: FaceHeuristic = self.heuristicCreator.getHeuristic(heuristic)
        for dirpath, dirnames, filenames in os.walk(folder):
            for filename in filenames:
                if self._isImage(filename):
                    facesCollection = faceHeuristic.filterFaces(
                        self.faceLocatorService.locate("%s/%s" % (folder,filename))
                    )
                    self.saveService.saveFaces(folder, filename, facesCollection, heuristic)
                    self.saveServiceJpg.saveFaces(folder, filename, facesCollection)
        self._moveFaces(folder)