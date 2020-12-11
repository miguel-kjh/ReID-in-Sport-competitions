import cv2
from retinaface.pre_trained_models import get_model
from Domain.Face import Face


class FacesLocatorService:

    def __init__(self):
        self.model = get_model("resnet50_2020-07-20",
                          max_size=2048)
        self.model.eval()

    def _createFace(self, id: int, annotations: dict):
        print(annotations)
        posX   = annotations['bbox'][0]
        posY   = annotations['bbox'][1]
        width  = annotations['bbox'][2]
        height = annotations['bbox'][3]
        return Face(id, posX, posY, width, height)

    def locator(self, id: int, file: str) -> Face:
        image = cv2.imread(file)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        annotations = self.model.predict_jsons(image)
        return self._createFace(id, annotations[0])
