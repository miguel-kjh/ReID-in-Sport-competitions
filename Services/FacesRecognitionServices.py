from deepface import DeepFace
import pandas as pd

class FacesRecognitionService:

    def __init__(self):
        self._models = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib"]

    def verifyImageInDataBase(self, img: str, dbPath: str, model: str = "VGG-Face", metric: str = "cosine") -> pd.DataFrame:
        if not model in self._models:
            return

        df = DeepFace.find(img, dbPath, model_name = model, distance_metric = metric, enforce_detection=False)
        return df