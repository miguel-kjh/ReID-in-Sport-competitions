from Services.AlignedReIDServices import AlignedReIDServices
from Services.SaveBodyPkl import SaveBodyPkl
from Utils.fileUtils import createFolder

class AlignedReIDController:

    def __init__(self):
        self._alignedService = AlignedReIDServices()
        self._folder = 'data/TCG_alignedReId'
        createFolder(self._folder)
        self._saveService = SaveBodyPkl(self._folder)

    def run(self, folder):
        embeddingCollection = self._alignedService.imgToEmbedding(folder)
        for filename, collection in embeddingCollection.items():
            self._saveService.saveBodyInformation(filename, collection)

