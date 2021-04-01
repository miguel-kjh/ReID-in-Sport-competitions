from deepface import DeepFace
from Utils.fileUtils import getNumber, getTime
from Utils.constant import COMPRESSION_FACTOR, MINIMUM_DURATION, PLACES_PROBE_TEST, PLACES, PLACES_GALLERY_TEST
from deepface.commons import distance as dst
from sklearn.decomposition import PCA
from Services.SaveEmbeddingPkl import SaveEmbeddingPkl

import ntpath
import numpy as np
import os

class FacesRecognitionService:

    def __init__(self, databaseFaces):
        self._loadServices = SaveEmbeddingPkl(databaseFaces)
        self._models  = ["VGG-Face", "Facenet", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib", "Ensemble"]
        self._metrics = {
            'cosine': dst.findCosineDistance,
            'euclidean': dst.findEuclideanDistance,
            'euclidean_l2': self._l2Dst
        }
        self._pca = PCA(n_components=COMPRESSION_FACTOR)

    def _l2Dst(self, first_emd: np.array, second_emd: np.array) -> float:
        return dst.findEuclideanDistance(
            dst.l2_normalize(first_emd),
            dst.l2_normalize(second_emd)
        )

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

    def _computeTemporalClassification(self, dateProbe, dateGallery, isOrder) -> bool:
        if isOrder:
            return dateProbe < dateGallery and abs(dateProbe - dateGallery) >= MINIMUM_DURATION
        else:
            return dateProbe > dateGallery and abs(dateProbe - dateGallery) >= MINIMUM_DURATION

    def checkMetricAndModel(self, model, metric):
        if model not in self._models:
            raise RuntimeError("The model for identification %s does not exist" % model)

        if metric not in self._metrics.keys():
            raise RuntimeError("The metric for identification %s does not exist" % metric)

    def verifyImageInDataBase(self, img: str, dbPath: str, model: str = "VGG-Face", metric: str = "cosine") -> list:

        self.checkMetricAndModel(model, metric)

        df = DeepFace.find(img, dbPath, model_name = model, distance_metric = metric, enforce_detection = False)

        return [getNumber(ntpath.basename(file)) for file in df['identity']]

    def reductionFacesDimension(self, embeddingFile: str, saveFolder: str):
        saveService = SaveEmbeddingPkl(saveFolder)
        embedding = saveService.loadInformation(embeddingFile)
        data = np.array([vector[1] for vector in embedding])
        data = self._pca.fit_transform(data)
        for index in range(len(embedding)):
            embedding[index][1] = data[index]
        saveService.saveFacesInformation(saveFolder, embedding)


    def computeClassification(self, probe: np.array, gallery: list, model_file: str,
                              metric: str = "cosine", temporalCoherence: bool = False,
                              isOrder: bool = True, filledGallery: bool = True) -> list:
        if temporalCoherence:
            distances = [
                (dorsal, self.computeDistance(embedding, probe[1], metric))
                for dorsal, embedding, galleryDate in gallery
                if self._computeTemporalClassification(getTime(os.path.basename(probe[0])), galleryDate, isOrder)
            ]
        else:
            distances = [
                (dorsal, self.computeDistance(embedding, probe[1], metric))
                for dorsal, embedding, _ in gallery
            ]

        if filledGallery:
            dorsals = [runner[0] for runner in distances]
            for index, place in enumerate(PLACES):
                if place is not PLACES_PROBE_TEST and index < PLACES.index(PLACES_GALLERY_TEST):
                    extra_gallery = self._loadServices.loadInformation(os.path.join(place, model_file.replace('.pkl', '')), ispath=False)
                    for file, embedding in extra_gallery:
                        dorsal = getNumber(os.path.basename(file))
                        if dorsal in dorsals:
                            distances.append(
                                (dorsal, self.computeDistance(embedding, probe[1], metric))
                            )

        distances.sort(key = lambda dist: dist[1])
        return [dorsal for dorsal, _ in distances]