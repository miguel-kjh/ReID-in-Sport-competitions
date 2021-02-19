from abc import abstractmethod
from Domain.BodyCollection import BodyCollection

class SaveBodyService:

    @abstractmethod
    def saveBodyInformation(self,
                  filename: str,
                  embediddingCollection: dict) -> None:
        pass

    @abstractmethod
    def loadBodyInformation(self, filename: str) -> BodyCollection:
        pass
