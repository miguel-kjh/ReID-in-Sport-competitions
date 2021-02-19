from Services.AlignedReIDServices import AlignedReIDServices
from Services.SaveBodyPkl import SaveBodyPkl

class AlignedReIDController:

    def __init__(self):
        self._alignedService = AlignedReIDServices()
        self._saveService = SaveBodyPkl()

    def run(self, folder):
        embeddingCollection = self._alignedService.imgToEmbedding(folder)
        for filename, collection in embeddingCollection.items():
            self._saveService.saveBodyInformation(filename, collection)

