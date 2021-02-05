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

    def _calculateAveragePrecision(self, dorsalList: list, query: int) -> tuple:
        averagePrecision = []
        count = 0

        for index, dorsal in enumerate(dorsalList):
            if dorsal == query:
                count += 1
                averagePrecision.append(count / (index + 1))
            else:
                averagePrecision.append(0)

        return averagePrecision[0], sum(averagePrecision)


    def identificationPeople(self, database: str, model: str, metric: str, topNum: int = 150) -> np.array:
        querysCount = 0
        matches = np.zeros(topNum)
        average_precision = {
            "top_1": [],
            "top_5": []
        }

        for dirpath, _, filenames in os.walk(database):
            for index, filename in enumerate(filenames):
                if index == 4: break
                if isImage(filename):
                    dorsal = getNumber(filename)

                    elementsList = list(chain.from_iterable([
                        self._recognition.verifyImageInDataBase(
                            os.path.join(dirpath, filename),
                            os.path.join(self.gallery, place),
                            model  = model,
                            metric = metric
                        )
                        for place in self.places
                    ]))

                    elementsList.sort(key=lambda element: element.distance)
                    dorsalList = [element.dorsal for element in elementsList]

                    try:
                        matches[dorsalList.index(dorsal)] += 1
                    except IndexError or ValueError:
                        matches[-1] += 0

                    countTP = 1 / dorsalList.count(dorsal)
                    avTop1, avTop5 = self._calculateAveragePrecision(dorsalList[0:5], dorsal)
                    average_precision["top_1"].append(countTP * avTop1)
                    average_precision["top_5"].append(countTP * avTop5)

                    querysCount += 1

        cmc = np.cumsum(matches) / querysCount

        return cmc, sum(average_precision["top_1"]) / querysCount, sum(average_precision["top_5"]) / querysCount


