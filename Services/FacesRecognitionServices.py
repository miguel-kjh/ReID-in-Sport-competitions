from deepface import DeepFace
import pandas as pd
from Utils.Utils import getNumber
import ntpath

class FacesRecognitionService:

    def __init__(self):
        self._models = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib"]

    def verifyImageInDataBase(self, img: str, dbPath: str, model: str = "VGG-Face", metric: str = "cosine") -> list:
        if not model in self._models:
            return

        df = DeepFace.find(img, dbPath, model_name = model, distance_metric = metric, enforce_detection=False)
        return [getNumber(ntpath.basename(file)) for file in df['identity']]