import cv2
import os
import shutil

from PIL import Image
import numpy as np

from Domain.FacesCollection import FacesCollection
from Services.SaveFacesServices import SaveFacesServices


class SaveFacesJpg(SaveFacesServices):

    def __init__(self):
        self.files = []

    def _clip(self, image: str, faces: FacesCollection) -> list:
        image = Image.open(image, 'r')
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return [image[face.posY:face.height, face.posX:face.width] for face in faces.facesCollection]

    def saveFaces(self, folder: str, filename: str, facesCollection: FacesCollection, heuristic: str = "none") -> None:
        for index, imageClipping in enumerate(self._clip("%s/%s" %(folder, filename), facesCollection)):
            try:
                newFilename = "%s/%s" %(folder, filename.replace('.jpg', '_%i_faces.jpg' % index))
                cv2.imwrite(newFilename, imageClipping)
                self.files.append(newFilename)
            except:
                continue