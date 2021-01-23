import cv2
import os

from PIL import Image
import numpy as np

from Domain.FacesCollection import FacesCollection
from Services.SaveFacesServices import SaveFacesServices


class SaveFacesJpg(SaveFacesServices):

    def __init__(self, facesFolder):
        self.facesFolder: str = facesFolder

    def _clip(self, image: str, faces: FacesCollection) -> list:
        image = Image.open(image, 'r')
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return [image[face.posY:face.height, face.posX:face.width] for face in faces.facesCollection]

    def saveFaces(self, folder: str, filename: str, facesCollection: FacesCollection) -> None:
        for index, imageClipping in enumerate(self._clip(os.path.join(folder, filename), facesCollection)):
            try:
                newFilename = os.path.join(self.facesFolder, filename.replace('.jpg', '_%i_faces.jpg' % index))
                cv2.imwrite(newFilename, imageClipping)
            except:
                continue