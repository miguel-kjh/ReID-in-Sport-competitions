from Services.AlignedReIDServices import AlignedReIDServices
from Services.SaveEmbeddingPkl import SaveEmbeddingPkl
from Utils.fileUtils import createFolder

class AlignedReIDController:

    def __init__(self):
        self._alignedService = AlignedReIDServices()
        self._folder = 'data/TCG_alignedReId'
        #createFolder(self._folder)
        self._saveService = SaveEmbeddingPkl(self._folder)

    def computedEmbeddings(self, folder: str, compression: bool = False):
        embedding_collection = self._alignedService.imgToEmbedding(folder, compression)
        for filename, collection in embedding_collection.items():
            if compression:
                filename = filename + "_pca"
            self._saveService.saveBodyInformation(filename, collection)

    def compactedEmbeddings(self, faces: str, bodies: str, filename: str, compression: bool = False):
        body_collection = self._saveService.loadInformation(bodies)
        faces_array = self._saveService.loadInformation(faces)

        self._alignedService.compactedEmbeddings(faces_array, body_collection, compression=compression)
        self._saveService.saveBodyInformation(filename, body_collection)