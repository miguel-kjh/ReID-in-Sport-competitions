import numpy as np
from Domain.BodyCollection import BodyCollection, Body
from Utils.distance import compute_dist
from Utils.utils import dtw
from Utils.re_ranking import re_ranking
import torch
from deepface.commons import distance as dst


class BodyRecognitionServices:

    def __init__(self):
        self._metrics = {
            'cosine': dst.findCosineDistance,
            'euclidean': dst.findEuclideanDistance
        }

    def _isDistance(self, metric: str) -> bool:
        return metric in self._metrics.keys()

    def _padVector(self, v1: np.array, v2: np.array) -> tuple:
        larger_dimension_vector  = v1 if v1.shape[0] > v2.shape[0] else v2
        smaller_dimension_vector = v1 if v1.shape[0] < v2.shape[0] else v2

        aux = np.zeros(larger_dimension_vector.shape)
        aux[:smaller_dimension_vector.shape[0]] = smaller_dimension_vector

        return larger_dimension_vector, aux

    def computeDistance(self, v1: np.array, v2: np.array, metric: str) -> float:
        if v1.shape[0] != v2.shape[0]:
            v1, v2 = self._padVector(v1, v2)

        return self._metrics[metric](v1, v2)

    def computeClassification(self, query: Body, gallery: BodyCollection, metric: str = "euclidean") -> list:
        if not self._isDistance(metric):
            raise ValueError("%s is not a distance function" % metric)

        if metric == 're-ranking':
            dist = [(galleryData.dorsal, dtw(re_ranking(torch.tensor(query.embedding),
                                                        torch.tensor(galleryData.embedding)))[0])
                    for galleryData in gallery.bodies]
        else:
            dist = [(galleryData.dorsal, dtw(compute_dist(query.embedding, galleryData.embedding, metric))[0])
                    for galleryData in gallery.bodies]

        dist.sort(key = lambda ele: ele[1])

        return [ runner[0] for runner in dist]

    def computeClassificationPCA(self, query: Body, gallery: BodyCollection, metric: str = "euclidean") -> list:
        if not self._isDistance(metric):
            raise ValueError("%s is not a distance function" % metric)

        dist = [(galleryData.dorsal, self.computeDistance(query.embedding, galleryData.embedding, metric))
                for galleryData in gallery.bodies]

        dist.sort(key = lambda ele: ele[1])

        return [ runner[0] for runner in dist ]