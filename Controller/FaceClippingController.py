import os

from Services.SaveFacesJpg import SaveFacesJpg
from Services.SaveFacesJson import SaveFacesJson
from Utils.Utils import createFolder


class FaceClippingController:

    def __init__(self, folderJson: str):
        self.saveServiceJson: SaveFacesJson = SaveFacesJson()
        self.gallery = folderJson.replace("TGC2020v0.3_json", "Gallery_faces")
        createFolder(self.gallery)
        self.saveServiceJpg: SaveFacesJpg = SaveFacesJpg(self.gallery)
        self.folderJson = folderJson

    def getImageClippings(self, folderImage: str):

        for dirpath, dirnames, filenames in os.walk(self.folderJson):
            for filename in filenames:
                fc = self.saveServiceJson.loadFaces(os.path.join(dirpath,filename))
                self.saveServiceJpg.saveFaces(
                    os.path.join(folderImage, os.path.basename(dirpath)),
                    filename.replace("json", "jpg"),
                    fc
                )