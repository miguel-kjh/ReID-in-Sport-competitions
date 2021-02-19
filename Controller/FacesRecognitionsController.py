import os
import numpy as np
from Services.FacesRecognitionServices import FacesRecognitionService
from Services.SaveBodyPkl import SaveBodyPkl
from Utils.fileUtils import getNumber
from Utils.distance import compute_dist
from Utils.utils import dtw
from statistics import mean

class FacesRecognitionsController:

    def __init__(self):
        self._recognition = FacesRecognitionService()
        self.facesGallery = "data/TGC_places"
        self.alignedGallery = "data/TCG_alignedReId"
        self._loadServices = SaveBodyPkl(self.alignedGallery)

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


    def identificationRunnersByFaces(self, probe: str, model: str, metric: str, galleryPlace: str, topNum: int = 107) -> tuple:
        querysCount = 0
        matches = np.zeros(topNum)
        average_precision = []

        actualGallery = os.path.join(self.facesGallery, galleryPlace)

        for dirpath, _, filenames_probe in os.walk(probe):

            for filename in filenames_probe:
                dorsal = getNumber(filename)

                classification = self._recognition.verifyImageInDataBase(
                    os.path.join(dirpath, filename),
                    actualGallery,
                    model  = model,
                    metric = metric
                )

                try:
                    matches[classification.index(dorsal)] += 1
                except Exception:
                    pass

                countTP = classification.count(dorsal)
                countTP = 0 if countTP == 0 else 1 / countTP
                ap = self._calculateAveragePrecision(classification, dorsal)
                average_precision.append(countTP * ap)
                querysCount += 1

        cmc = np.cumsum(matches) / querysCount

        return cmc, sum(average_precision) / querysCount

    def identificationRunnersByBody(self, probe: str, metric: str, galleryPlace: str, topNum: int = 107) -> tuple:
        matches = np.zeros(topNum)
        average_precision = []

        probe = self._loadServices.loadBodyInformation(probe)
        gallery = self._loadServices.loadBodyInformation(galleryPlace)

        for query in probe.bodies:
            dist = [(galleryData.dorsal, dtw(compute_dist(query.embedding, galleryData.embedding, metric))[0])
                    for galleryData in gallery.bodies]
            dist.sort(key = lambda ele: ele[1])

            classification = [ runner[0] for runner in dist]

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


