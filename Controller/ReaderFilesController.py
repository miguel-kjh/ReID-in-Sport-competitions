import os

from Services.RetinaFaceLocatorService import RetinaFacesLocatorService
from Services.Img2PoseLocatorService import Img2PoseLocatorService
from Services.SaveFacesJson import SaveFacesJson
from Services.SaveFacesJpg import SaveFacesJpg
from Utils.Heuristics.FaceHeuristic import FaceHeuristic
from Utils.Heuristics.HeuristicCreator import HeuristicCreator
from Utils.Utils import isImage

class ReaderFilesController:
    def __init__(self):
        self.saveService: SaveFacesJson = SaveFacesJson()
        self.saveServiceJpg: SaveFacesJpg = SaveFacesJpg()
        self.faceLocatorService: RetinaFacesLocatorService = RetinaFacesLocatorService()
        #self.faceLocatorService: Img2PoseLocatorService = Img2PoseLocatorService()
        self.heuristicCreator: HeuristicCreator = HeuristicCreator()

    def run(self, folder: str, heuristic: str = 'none') -> None:
        faceHeuristic: FaceHeuristic = self.heuristicCreator.getHeuristic(heuristic)
        for dirpath, dirnames, filenames in os.walk(folder):
            for filename in filenames:
                if isImage(filename):
                    facesCollection = faceHeuristic.filterFaces(
                        self.faceLocatorService.locate(os.path.join(folder,filename))
                    )
                    self.saveService.saveFaces(folder, filename, facesCollection, heuristic)
                    self.saveServiceJpg.saveFaces(folder, filename, facesCollection)
