import os
import numpy as np
from Services.FacesRecognitionServices import FacesRecognitionService
from Utils.Utils import getNumber

class FacesRecognitionsController:

    def __init__(self):
        self._recognition = FacesRecognitionService()
        self.gallery = "data/TGC_places"

    def _calculateAveragePrecision(self, dorsalList: list, query: int) -> tuple:
        if not dorsalList or query not in dorsalList:
            return 0., 0.

        averagePrecision = []
        count = 0

        for index, dorsal in enumerate(dorsalList):
            if dorsal == query:
                count += 1
                averagePrecision.append(count / (index + 1))

        return averagePrecision[0], sum(averagePrecision)


    def identificationPeople(self, probe: str, model: str, metric: str, galleryPlace: str, topNum: int = 107) -> tuple:
        querysCount = 0
        matches = np.zeros(topNum)
        average_precision = {
            "top_1": [],
            "top_5": []
        }

        actualGallery = os.path.join(self.gallery, galleryPlace)

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
                avTop1, avTop5 = self._calculateAveragePrecision(classification[0:5], dorsal)
                average_precision["top_1"].append(countTP * avTop1)
                average_precision["top_5"].append(countTP * avTop5)

                querysCount += 1

        cmc = np.cumsum(matches) / querysCount

        return cmc, sum(average_precision["top_1"]) / querysCount, sum(average_precision["top_5"]) / querysCount


