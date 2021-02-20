from abc import abstractmethod

class SaveEmbeddingService:

    @abstractmethod
    def saveBodyInformation(self,
                  filename: str,
                  embediddingCollection: dict) -> None:
        pass

    @abstractmethod
    def loadInformation(self, filename: str):
        pass
