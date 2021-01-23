import os
import ntpath

from Services.FacesRecognitionServices import FacesRecognitionService
from Utils.Statistics.RunnersStats import RunnersStats
from Utils.Utils import isImage,getPlace,getNumber,findFile

class FacesRecognitionsController:

    def __init__(self):
        self._recognition = FacesRecognitionService()
        self.gallery = "data/TGC_places"

    def identificationPeople(self, database: str) -> RunnersStats:
        runners = RunnersStats()
        for dirpath, _, filenames in os.walk(database):
            for filename in filenames:
                if isImage(filename):
                    dorsal = getNumber(filename)
                    place  = getPlace(filename)

                    if not runners.isRunner(dorsal):
                        runners.addRunner(dorsal)

                    df = self._recognition.verifyImageInDataBase(os.path.join(dirpath, filename), os.path.join(self.gallery, place))
                    dorsalIdentified = None if df.empty else getNumber(ntpath.basename(df['identity'][0]))
                    if dorsalIdentified:
                        runners.addPosition(dorsal, place, dorsalIdentified)

        return runners


