from deepface import DeepFace
from Utils.fileUtils import getNumber
from deepface.commons import distance as dst

import ntpath
import numpy as np

class ElementRunnersRanking:
    def __init__(self, dorsal: int, distance: float):
        self.dorsal   = dorsal
        self.distance = distance

class FacesRecognitionService:

    def __init__(self):
        self._models  = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "Ensemble"]
        self._metrics = {
            'cosine': dst.findCosineDistance,
            'euclidean': dst.findEuclideanDistance,
            'euclidean_l2': self._l2Dst
        }

    def _l2Dst(self, first_emd: np.array, second_emd: np.array) -> float:
        return dst.findEuclideanDistance(
            dst.l2_normalize(first_emd),
            dst.l2_normalize(second_emd)
        )

    def checkMetricAndModel(self, model, metric):
        if model not in self._models:
            raise RuntimeError("The model for identification %s does not exist" % model)

        if metric not in self._metrics.keys():
            raise RuntimeError("The metric for identification %s does not exist" % metric)

    def verifyImageInDataBase(self, img: str, dbPath: str, model: str = "VGG-Face", metric: str = "cosine") -> list:

        self.checkMetricAndModel(model, metric)

        df = DeepFace.find(img, dbPath, model_name = model, distance_metric = metric, enforce_detection = False)

        return [getNumber(ntpath.basename(file)) for file in df['identity']]

    def computeClassification(self, probe: np.array, gallery: list, metric: str = "cosine") -> list:
        distances = [
            (dorsal, self._metrics[metric](probe, embedding))
            for dorsal, embedding in gallery
        ]

        distances.sort(key = lambda dist: dist[1])
        return [dorsal for dorsal, _ in distances]