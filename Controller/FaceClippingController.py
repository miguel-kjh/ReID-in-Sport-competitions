import os

from Services.SaveFacesJpg import SaveFacesJpg
from Services.SaveFacesJson import SaveFacesJson
from Utils.fileUtils import createFolder
from Utils.constant import PLACES


class FaceClippingController:

    def __init__(self, folderJson: str):
        self.saveServiceJson: SaveFacesJson = SaveFacesJson()
        self.probe = folderJson.replace("TGC2020v0.3_json", "Probe_faces")
        createFolder(self.probe)
        self.saveServiceJpg: SaveFacesJpg = SaveFacesJpg(self.probe)
        self.folderJson = folderJson

        for place in PLACES:
            createFolder(os.path.join(self.probe, place))

    def getImageClippings(self, folderImage: str):

        for dirpath, dirnames, filenames in os.walk(self.folderJson):
            for filename in filenames:
                fc = self.saveServiceJson.loadFaces(os.path.join(dirpath,filename))
                self.saveServiceJpg.saveFaces(
                    os.path.join(folderImage, os.path.basename(dirpath)),
                    filename.replace("json", "jpg"),
                    fc
                )