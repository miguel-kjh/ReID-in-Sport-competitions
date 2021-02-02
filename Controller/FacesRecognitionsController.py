import os
import numpy as np
from itertools import chain

from Services.FacesRecognitionServices import FacesRecognitionService
from Utils.Utils import isImage, getPlace, getNumber

class FacesRecognitionsController:

    def __init__(self):
        self._recognition = FacesRecognitionService()
        self.gallery      = "data/TGC_places"
        self.places       = ["Arucas", "Ayagaures", "ParqueSur", "PresaDeHornos", "Teror"]

    def _calculateMeanAPTopK(self, cmc: np.array, topK: int) -> float:
        return 1.

    def identificationPeople(self, database: str, model: str, metric: str, topNum: int = 1500) -> np.array:
        embeddingCount = 0
        matches = np.zeros(topNum)

        for dirpath, _, filenames in os.walk(database):
            for filename in filenames:
                if isImage(filename):
                    dorsal = getNumber(filename)
                    sourcePlace  = getPlace(filename)

                    dorsalList = list(chain.from_iterable([
                        self._recognition.verifyImageInDataBase(
                            os.path.join(dirpath, filename),
                            os.path.join(self.gallery, place),
                            model  = model,
                            metric = metric
                        )
                        for place in self.places
                        #if place != sourcePlace
                    ]))
                    dorsalList.sort(key=lambda x: x[1])
                    dorsalList = [dorsal for dorsal, _ in dorsalList]
                    matches[dorsalList.index(dorsal)] += 1
                    embeddingCount += 1

        cmc = np.cumsum(matches) / embeddingCount

        return cmc, self._calculateMeanAPTopK(cmc, 1), self._calculateMeanAPTopK(cmc, 5)


