import os
import re

from Services.FacesRecognitionServices import FacesRecognitionService
from Utils.Statistics.RunnersStats import RunnersStats

class FacesRecognitionsController:

    def __init__(self):
        self._recognition = FacesRecognitionService()
        self.gallery = "../data/TGC_places"
        #self.places  = ["Arucas", "Ayagaures", "ParqueSur", "PresaDeHornos", "Teror"]

    def _getPlace(self, filename: str) -> str:
        match = re.search(r'\d+_(\w+)_f', filename)
        return match.group(1)

    def _getNumber(self, filename: str) -> int:
        return int(filename[0])

    def identificationPeople(self, database: str) -> list:
        #df = self._recognition.verifyImageInDataBase(personToSearch, database)
        #return df['identity'][0] if not df.empty else ''
        runners = RunnersStats()
        for dirpath, dirnames, filenames in os.walk(database):
            for filename in filenames:
                dorsal = self._getNumber(filename)
                place  = self._getPlace(filename)
                if not runners.isRunner(dorsal):
                    runners.addRunner(dorsal)
                print(os.path.join(dirpath, filename),  os.path.join(self.gallery, place))
                df = self._recognition.verifyImageInDataBase(os.path.join(dirpath, filename), os.path.join(self.gallery, place))
                dorsalIdentified = df['identity'][0] if not df.empty else 0
                runners.addPosition(dorsal, place, dorsalIdentified)
                break
        print(runners)
        return runners


