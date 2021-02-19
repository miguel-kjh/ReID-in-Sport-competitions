from Domain.BodyCollection import BodyCollection
from Services.SaveBodyService import SaveBodyService
from Utils.fileUtils import createFolder

import pickle
import os

class SaveBodyPkl(SaveBodyService):

    def __init__(self):
        self._folder = 'data/TCG_alignedReId'
        createFolder(self._folder)

    def saveBodyInformation(self, filename: str, collection: BodyCollection) -> None:
        with open(os.path.join(self._folder, "%s.pkl" %filename), 'wb') as output:
            pickle.dump(collection, output, pickle.HIGHEST_PROTOCOL)

    def loadBodyInformation(self, filename: str) -> BodyCollection:
        pass