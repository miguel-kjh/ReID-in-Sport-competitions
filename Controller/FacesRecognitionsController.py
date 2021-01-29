import os
import ntpath
import numpy as np

from Services.FacesRecognitionServices import FacesRecognitionService
from Utils.Statistics.RunnersStats import RunnersStats
from Utils.Utils import isImage,getPlace,getNumber

class FacesRecognitionsController:

    def __init__(self):
        self._recognition = FacesRecognitionService()
        self.gallery = "data/TGC_places"

    def identificationPeople(self, database: str, model: str, metric: str, topNum: int = 100) -> np.array:
        embeddingCount = 0
        matches = np.zeros(topNum)

        for dirpath, _, filenames in os.walk(database):
            for filename in filenames:
                if isImage(filename):
                    dorsal = getNumber(filename)
                    place  = getPlace(filename)

                    dorsalList = self._recognition.verifyImageInDataBase(
                        os.path.join(dirpath, filename),
                        os.path.join(self.gallery, place),
                        model  = model,
                        metric = metric
                    )

                    for rank in range(topNum):
                        if dorsalList[rank] == dorsal:
                            matches[rank] += 1
                            break
                    embeddingCount += 1

        return np.cumsum(matches) / embeddingCount


