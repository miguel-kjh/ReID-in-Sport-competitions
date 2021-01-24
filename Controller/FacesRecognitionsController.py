import os
import ntpath

from Services.FacesRecognitionServices import FacesRecognitionService
from Utils.Statistics.RunnersStats import RunnersStats
from Utils.Utils import isImage,getPlace,getNumber

class FacesRecognitionsController:

    def __init__(self):
        self._recognition = FacesRecognitionService()
        self.gallery = "data/TGC_places"

    def identificationPeople(self, database: str, model: str, metric: str) -> RunnersStats:
        runners = RunnersStats()
        for dirpath, _, filenames in os.walk(database):
            for filename in filenames:
                if isImage(filename):
                    dorsal = getNumber(filename)
                    place  = getPlace(filename)

                    if not runners.isRunner(dorsal):
                        runners.addRunner(dorsal)

                    dorsalList = self._recognition.verifyImageInDataBase(
                        os.path.join(dirpath, filename),
                        os.path.join(self.gallery, place),
                        model = model,
                        metric = metric
                    )
                    try:
                        position = dorsalList.index(dorsal) + 1
                    except ValueError:
                        position = -1

                    runners.addPosition(dorsal, place, position)

        return runners


