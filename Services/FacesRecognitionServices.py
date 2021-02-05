from deepface import DeepFace
from Utils.Utils import getNumber
import ntpath

class ElementRunnersRanking:
    def __init__(self, dorsal: int, distance: float):
        self.dorsal   = dorsal
        self.distance = distance

class FacesRecognitionService:

    def __init__(self):
        self._models = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "Ensemble"]

    def verifyImageInDataBase(self, img: str, dbPath: str, model: str = "VGG-Face", metric: str = "cosine") -> list:
        if model not in self._models:
            raise RuntimeError("The model for identification %s does not exist" % model)

        df = DeepFace.find(img, dbPath, model_name = model, distance_metric = metric, enforce_detection = False)

        return [ElementRunnersRanking(getNumber(ntpath.basename(file)),distance)
                for file, distance in zip(df['identity'], df["%s_%s" %(model, metric)])]