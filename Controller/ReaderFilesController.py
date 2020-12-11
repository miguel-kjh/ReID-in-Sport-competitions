import os
import re

from Services.FaceLocatorService import FacesLocatorService
from Services.SaveFacesJson import SaveFacesJson

class ReaderFilesController:
    def __init__(self):
        self.saveService: SaveFacesJson = SaveFacesJson()
        self.faceLocatorService: FacesLocatorService = FacesLocatorService()

    def run(self, folder: str) -> None:
        print(folder)
        for dirpath, dirnames, filenames in os.walk(folder):
            for filename in filenames:
                if re.search(".jpg$", filename):
                    facesCollection = self.faceLocatorService.locate("%s/%s" % (folder,filename))
                    self.saveService.saveFaces(folder, filename, facesCollection)