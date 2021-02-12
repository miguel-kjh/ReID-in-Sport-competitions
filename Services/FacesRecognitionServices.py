from deepface import DeepFace
from Utils.Utils import getNumber
import ntpath

class ElementRunnersRanking:
    def __init__(self, dorsal: int, distance: float):
        self.dorsal   = dorsal
        self.distance = distance

class FacesRecognitionService:

    def __init__(self):
        self._models  = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "Ensemble"]
        self._metrics = ['cosine', 'euclidean', 'euclidean_l2']

    def _checkMetricAndModel(self, model, metric):
        if model not in self._models:
            raise RuntimeError("The model for identification %s does not exist" % model)

        if metric not in self._metrics:
            raise RuntimeError("The metric for identification %s does not exist" % metric)

    def verifyImageInDataBase(self, img: str, dbPath: str, model: str = "VGG-Face", metric: str = "cosine") -> list:

        self._checkMetricAndModel(model, metric)

        df = DeepFace.find(img, dbPath, model_name = model, distance_metric = metric, enforce_detection = False)

        return [getNumber(ntpath.basename(file)) for file in df['identity']]