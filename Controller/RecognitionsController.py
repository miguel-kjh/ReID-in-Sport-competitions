from Services.FacesRecognitionServices import FacesRecognitionService
from Services.BodyRecognitionServices import BodyRecognitionServices
from Services.SaveEmbeddingPkl import SaveEmbeddingPkl
from Utils.fileUtils import getNumber, getTime
from Utils.constant import PLACES

from statistics import mean

import os
import numpy as np

class RecognitionsController:

    def __init__(self):
        self._face_recognition = FacesRecognitionService()
        self._body_recognition = BodyRecognitionServices()
        self.facesGallery = "data/TGC_places"
        self.alignedGallery = "data/TCG_alignedReId"
        self._loadServices = SaveEmbeddingPkl(self.alignedGallery)

    def _calculateAveragePrecision(self, dorsalList: list, query: int) -> float:
        if not dorsalList or query not in dorsalList:
            return 0.

        averagePrecision = []
        count = 0

        for index, dorsal in enumerate(dorsalList):
            if dorsal == query:
                count += 1
                averagePrecision.append(count / (index + 1))

        return sum(averagePrecision)


    def identificationRunnersByFaces(self, probe: str, model: str, metric: str,
                                     galleryPlace: str, topNum: int = 107,
                                     pca: bool = False, temporalCoherence: bool = False) -> tuple:

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
            classification = self._face_recognition.computeClassification(query, gallery,
                                                                          metric = metric,
                                                                          temporalCoherence=temporalCoherence,
                                                                          isOrder=isOrder)
            try:
                matches[classification.index(dorsal)] += 1
            except Exception:
                pass

            countTP = classification.count(dorsal)
            countTP = 0 if countTP == 0 else 1 / countTP
            ap = self._calculateAveragePrecision(classification, dorsal)
            average_precision.append(countTP * ap)

        cmc = np.cumsum(matches) / len(probes)

        return cmc, sum(average_precision) / len(probes)

    def identificationRunnersByBody(self, probe: str, metric: str, galleryPlace: str, topNum: int = 107) -> tuple:
        matches = np.zeros(topNum)
        average_precision = []

        probe = self._loadServices.loadInformation(probe)
        gallery = self._loadServices.loadInformation(galleryPlace)

        for query in probe.bodies:

            classification = self._body_recognition.computeClassification(query, gallery, metric)


            try:
                matches[classification.index(query.dorsal)] += 1
            except Exception:
                pass

            countTP = classification.count(query.dorsal)
            countTP = 0 if countTP == 0 else 1 / countTP
            ap = self._calculateAveragePrecision(classification, query.dorsal)
            average_precision.append(countTP * ap)

        cmc = np.cumsum(matches) / len(probe.bodies)
        return cmc, mean(average_precision)




