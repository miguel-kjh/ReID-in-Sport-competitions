from Domain.BodyCollection import BodyCollection
from Services.SaveEmbeddingService import SaveEmbeddingService
from Utils.fileUtils import createFolder

import pickle
import os

class SaveEmbeddingPkl(SaveEmbeddingService):

    def __init__(self, folder):
        self._folder = folder

    def saveBodyInformation(self, filename: str, collection: BodyCollection) -> None:
        with open(os.path.join(self._folder, "%s.pkl" %filename), 'wb') as output:
            pickle.dump(collection, output, pickle.HIGHEST_PROTOCOL)

    def loadInformation(self, filename: str):
        with open(filename, 'rb') as f:
            collection = pickle.load(f)

        return collection