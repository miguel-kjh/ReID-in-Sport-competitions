import os

from Services.SaveFacesJpg import SaveFacesJpg
from Services.SaveFacesJson import SaveFacesJson


class FaceClippingController:

    def __init__(self):
        self.saveServiceJson: SaveFacesJson = SaveFacesJson()


    def getImageClippings(self, folderJson: str, folderImage: str):

        print(folderJson)
        for dirpath, dirnames, filenames in os.walk(folderJson):
            for filename in filenames:
                fc = self.saveServiceJson.loadFaces(os.path.join(dirpath,filename))
                print(fc)