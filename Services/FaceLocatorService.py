import cv2
from retinaface.pre_trained_models import get_model
from Domain.Face import Face
from Domain.FacesCollection import FacesCollection


class FacesLocatorService:

    def __init__(self):
        self.model = get_model(
            "resnet50_2020-07-20",
            max_size=2048)
        self.model.eval()

    def _createFaces(self, annotations: dict) -> FacesCollection:
        collection = FacesCollection()
        if annotations:
            for id, annotation in enumerate(annotations):
                if annotation['bbox']:
                    posX   = annotation['bbox'][0]
                    posY   = annotation['bbox'][1]
                    width  = annotation['bbox'][2]
                    height = annotation['bbox'][3]
                    collection.addFace(Face(id, posX, posY, width, height))
        return collection

    def locate(self, file: str) -> FacesCollection:
        image = cv2.imread(file)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        annotations = self.model.predict_jsons(image)
        return self._createFaces(annotations)
