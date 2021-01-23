import os

from Services.RetinaFaceLocatorService import RetinaFacesLocatorService
from Services.Img2PoseLocatorService import Img2PoseLocatorService
from Services.SaveFacesJson import SaveFacesJson
from Services.SaveFacesJpg import SaveFacesJpg
from Utils.Heuristics.FaceHeuristic import FaceHeuristic
from Utils.Heuristics.HeuristicCreator import HeuristicCreator
from Utils.Utils import isImage, createFolder

class ReaderFilesController:

    def _createNameFolder(self, database, model, heuristic):
        return "%s_%s_%s" %(database, model, heuristic)

    def __init__(self, heuristic: str = 'none', model: str = 'retinaface'):

        if model == 'retinaface':
            self.faceLocatorService: RetinaFacesLocatorService = RetinaFacesLocatorService()
        elif model == 'img2pose':
            self.faceLocatorService: Img2PoseLocatorService = Img2PoseLocatorService()
        else:
            msg = "The model %s does not exist" %model
            raise Exception(msg)

        self.heuristicCreator: HeuristicCreator = HeuristicCreator()

        self.databaseJson  = os.path.join("data", "TGC2020v0.3_json")
        self.databaseFaces = os.path.join("data", "TGC2020v0.3_face")
        self.heuristic     = heuristic

        self.gallery     = self._createNameFolder(self.databaseJson, model, heuristic)
        self.facesFolder = self._createNameFolder(self.databaseFaces, model, heuristic)

        createFolder(self.gallery)
        createFolder(self.gallery)

        self.saveServiceJson: SaveFacesJson = SaveFacesJson()
        self.saveServiceJpg: SaveFacesJpg   = SaveFacesJpg(self.facesFolder)

    def run(self, folder: str) -> None:
        faceHeuristic: FaceHeuristic = self.heuristicCreator.getHeuristic(self.heuristic)

        db = os.path.join(self.gallery, os.path.basename(folder))
        os.mkdir(db)

        print(folder)
        for dirpath, dirnames, filenames in os.walk(folder):
            for filename in filenames:
                if isImage(filename):
                    facesCollection = faceHeuristic.filterFaces(
                        self.faceLocatorService.locate(os.path.join(folder,filename))
                    )
                    self.saveServiceJson.saveFaces(db, filename, facesCollection)

