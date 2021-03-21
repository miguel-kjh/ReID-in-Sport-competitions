import cv2
from retinaface.pre_trained_models import get_model
from Domain.Face import Face
from Domain.FacesCollection import FacesCollection
from Services.FacesLocator import FacesLocator
from Utils.constant import FACE_ENHANCEMENT_FACTOR
import torch


class RetinaFacesLocatorService(FacesLocator):

    def __init__(self):
        device: str = str(torch.device("cuda" if torch.cuda.is_available() else "cpu"))
        self.model = get_model(
            "resnet50_2020-07-20",
            max_size=2048,
            device=device)
        self.model.eval()

    def _createFaces(self, annotations: dict) -> FacesCollection:
        collection = FacesCollection(model = "RetinaFaces")
        if annotations:
            for id, annotation in enumerate(annotations):
                if annotation['bbox']:
                    posX   = annotation['bbox'][0]
                    #if posX < 0: posX = 0
                    posY   = annotation['bbox'][1]
                    #if posY < 0: posY = 0
                    width  = annotation['bbox'][2]
                    height = annotation['bbox'][3]
                    collection.addFace(Face(id, posX, posY, width, height, annotation['score']))
        return collection

    def locate(self, file: str) -> FacesCollection:
        image = cv2.imread(file)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        annotations = self.model.predict_jsons(image)
        return self._createFaces(annotations)
