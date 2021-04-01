from Domain.BodyCollection import BodyCollection
from Services.SaveEmbeddingService import SaveEmbeddingService

import pickle
import numpy as np
import os

class SaveEmbeddingPkl(SaveEmbeddingService):

    def __init__(self, folder):
        self._folder = folder

    def saveBodyInformation(self, filename: str, collection: BodyCollection) -> None:
        with open(os.path.join(self._folder, "%s.pkl" %filename), 'wb') as output:
            pickle.dump(collection, output, pickle.HIGHEST_PROTOCOL)

    def loadInformation(self, filename: str, ispath: bool = True):
        if ispath:
            with open(filename, 'rb') as f:
                collection = pickle.load(f)
        else:
            with open(os.path.join(self._folder, "%s.pkl" %filename), 'rb') as f:
                collection = pickle.load(f)
        return collection

    def saveFacesInformation(self, filename: str, collection):
        with open(filename, 'wb') as output:
            pickle.dump(collection, output, pickle.HIGHEST_PROTOCOL)