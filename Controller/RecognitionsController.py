from Services.FacesRecognitionServices import FacesRecognitionService
from Services.BodyRecognitionServices import BodyRecognitionServices
from Services.SaveEmbeddingPkl import SaveEmbeddingPkl
from Utils.fileUtils import getNumber, getTime
from Utils.constant import PLACES
from sklearn.metrics import average_precision_score, precision_recall_curve, auc

import os
import numpy as np

class RecognitionsController:

    def __init__(self, databaseFaces: str = ""):
        self._face_recognition = FacesRecognitionService(databaseFaces)
        self._body_recognition = BodyRecognitionServices()
        self.alignedGallery = "data/TCG_alignedReId"
        self._loadServices = SaveEmbeddingPkl(self.alignedGallery)

    def _calculateAveragePrecision(self, dorsalList: list, dist: list,  query: int) -> float:
        if not dorsalList or query not in dorsalList:
            return 0.

        """averagePrecision = []
        count = 0

        for index, dorsal in enumerate(dorsalList):
            if dorsal == query:
                count += 1
                averagePrecision.append(count / (index + 1))
        return sum(averagePrecision)"""
        gallery_match = np.array([1 if i == query else 0 for i in dorsalList])
        dist = np.array(dist)
        similarity = 1 - dist / np.amax(dist)
        return average_precision_score(gallery_match, similarity, average='macro', pos_label=1)


    def identificationRunnersByFaces(self, probe: str, model: str, metric: str,
                                     galleryPlace: str, topNum: int = 107,
                                     pca: bool = False, temporalCoherence: bool = False, filling: bool = False) -> tuple:

        self._face_recognition.checkMetricAndModel(model, metric)

        matches = np.zeros(topNum)
        average_precision = []
        isOrder = PLACES.index(os.path.basename(probe)) < PLACES.index(os.path.basename(galleryPlace))

        model_file = "representations_%s.pkl" % (model if not pca else "%s_pca" % model).lower().replace("-", "_")
        probe = os.path.join(probe, model_file)
        gallery = os.path.join(galleryPlace, model_file)

        probes = self._loadServices.loadInformation(probe)
        gallery = [(getNumber(os.path.basename(file)), embedding, getTime(os.path.basename(file)))
                   for file, embedding in self._loadServices.loadInformation(gallery)]

        for query in probes:
            dorsal = getNumber(os.path.basename(query[0]))
            classification, dist = self._face_recognition.computeClassification(query, gallery, model_file,
                                                                          metric = metric,
                                                                          temporalCoherence=temporalCoherence,
                                                                          isOrder=isOrder,
                                                                          filledGallery=filling)
            try:
                matches[classification.index(dorsal)] += 1
            except Exception:
                pass

            average_precision.append(
                self._calculateAveragePrecision(classification, dist, dorsal)
            )

        cmc = np.cumsum(matches) / len(probes)

        return cmc, np.mean(average_precision)

    def identificationRunnersByBody(self, probe: str, metric: str, galleryPlace: str,
                                    topNum: int = 107, temporalCoherence: bool = False,
                                    filling: bool = False, model: str = "") -> tuple:
        matches = np.zeros(topNum)
        average_precision = []
        isOrder = PLACES.index(os.path.basename(probe).replace(".pkl", '').split('_')[0]) \
                  < PLACES.index(os.path.basename(galleryPlace).replace(".pkl", '').split('_')[0])

        probe = self._loadServices.loadInformation(probe)
        gallery = self._loadServices.loadInformation(galleryPlace)

        for query in probe.bodies:

            classification, dist = self._body_recognition.computeClassification(query,
                                                                          gallery,
                                                                          metric,
                                                                          temporalCoherence=temporalCoherence,
                                                                          isOrder=isOrder,
                                                                          filledGallery=filling,
                                                                          model=model)


            try:
                matches[classification.index(query.dorsal)] += 1
            except Exception:
                pass

            average_precision.append(
                self._calculateAveragePrecision(classification, dist, query.dorsal)
            )

        cmc = np.cumsum(matches) / len(probe.bodies)
        return cmc, np.mean(average_precision)




